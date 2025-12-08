
#!/usr/bin/env python3
"""
Export comb_edge_node rows to NIH Translator DGX JSON format.

Usage:
    python export_to_dgx.py \
        --host localhost \
        --user myuser \
        --password mypass \
        --database mydb \
        --study-id 1 \
        --limit 1000 \
        --output magma_alz_dgx.json
"""

# imports
import argparse
import json
import sys
from typing import Dict, Any, List

import mysql.connector
from mysql.connector import Error



# constants

# methods
def get_connection(host: str, user: str, password: str, database: str):
    return mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database,
    )


def fetch_edges(conn, study_id: int, limit: int = None) -> List[Dict[str, Any]]:
    """
    Run the query with column aliases so we can access them cleanly.
    """
    query = """
        SELECT
            CONCAT(ed.edge_id, so.ontology_id, ta.ontology_id) AS edge_id,
            so.ontology_id  AS subject_id,
            ta.ontology_id  AS object_id,
            ed.score        AS score,
            sco_type.type_name AS score_type,
            so.node_name    AS subject_name,
            ta.node_name    AS object_name,
            ted.type_name   AS predicate,
            tso.type_name   AS subject_category,
            tta.type_name   AS object_category,
            ed.study_id     AS study_id,
            ed.publication_ids AS publication_ids,
            ed.score_translator AS score_translator,
            ed.id           AS internal_id
        FROM comb_edge_node ed
        JOIN comb_node_ontology so ON ed.source_node_id = so.id
        JOIN comb_node_ontology ta ON ed.target_node_id = ta.id
        JOIN comb_lookup_type ted ON ed.edge_type_id   = ted.type_id
        JOIN comb_lookup_type tso ON so.node_type_id   = tso.type_id
        JOIN comb_lookup_type tta ON ta.node_type_id   = tta.type_id
        JOIN comb_lookup_type sco_type ON ed.score_type_id = sco_type.type_id
        WHERE ed.study_id = %s
    """

    if limit is not None and limit > 0:
        query = query + " LIMIT %s"

    cursor = conn.cursor(dictionary=True)
    try:
        if limit is not None and limit > 0:
            cursor.execute(query, (study_id, limit))
        else:
            cursor.execute(query, (study_id,))
        rows = cursor.fetchall()
        return rows
    finally:
        cursor.close()


def parse_publication_ids(pub_ids) -> List[str]:
    """
    Convert publication_ids column into a list.
    Assumes values are either NULL, a single ID, or a comma/semicolon-separated list.
    """
    if pub_ids is None:
        return []

    if isinstance(pub_ids, (int, float)):
        return [str(pub_ids)]

    text = str(pub_ids).strip()
    if not text:
        return []

    # Split on comma or semicolon
    if "," in text:
        parts = [p.strip() for p in text.split(",")]
    elif ";" in text:
        parts = [p.strip() for p in text.split(";")]
    else:
        parts = [text]

    return [p for p in parts if p]


def build_dgx_graph(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Build a DGX-style graph structure from DB rows.

    Schema assumption (adjust as needed for your DGX environment):

    {
      "nodes": {
        "CURIE1": {
          "id": "CURIE1",
          "name": "Some Name",
          "categories": ["biolink:Gene"]
        },
        ...
      },
      "edges": {
        "edge_id123": {
          "id": "edge_id123",
          "subject": "NCBIGene:154664",
          "object": "MONDO:0004975",
          "predicate": "biolink:gene_associated_with_condition",
          "attributes": [
            {
              "attribute_type_id": "biolink:p_value",
              "value": 0.91881,
              "original_attribute_name": "score"
            },
            {
              "attribute_type_id": "translator:score_normalized",
              "value": 0.1976068345
            },
            {
              "attribute_type_id": "biolink:publication",
              "value": ["PMID:...", ...]
            }
          ]
        },
        ...
      }
    }
    """
    nodes: Dict[str, Dict[str, Any]] = {}
    edges: Dict[str, Dict[str, Any]] = {}

    for row in rows:
        edge_id = row["edge_id"]

        subj_id = row["subject_id"]
        obj_id = row["object_id"]

        subj_name = row["subject_name"]
        obj_name = row["object_name"]

        subj_cat = row["subject_category"]
        obj_cat = row["object_category"]

        predicate = row["predicate"]

        score = row["score"]
        score_type = row["score_type"]
        score_translator = row["score_translator"]
        study_id = row["study_id"]
        internal_id = row["internal_id"]

        pub_ids_list = parse_publication_ids(row["publication_ids"])

        # --- Nodes ---

        if subj_id not in nodes:
            nodes[subj_id] = {
                "id": subj_id,
                "name": subj_name,
                "categories": [subj_cat] if subj_cat else [],
            }

        if obj_id not in nodes:
            nodes[obj_id] = {
                "id": obj_id,
                "name": obj_name,
                "categories": [obj_cat] if obj_cat else [],
            }

        # --- Edge attributes ---

        attributes = []

        # Raw score (often a p-value)
        if score is not None:
            attributes.append(
                {
                    "attribute_type_id": score_type or "translator:score",
                    "value": float(score),
                    "original_attribute_name": "score",
                }
            )

        # Translator-normalized score
        if score_translator is not None:
            attributes.append(
                {
                    "attribute_type_id": "translator:score_normalized",
                    "value": float(score_translator),
                    "original_attribute_name": "score_translator",
                }
            )

        # Publications, if present
        if pub_ids_list:
            attributes.append(
                {
                    "attribute_type_id": "biolink:publication",
                    "value": pub_ids_list,
                    "original_attribute_name": "publication_ids",
                }
            )

        # Study / provenance info
        attributes.append(
            {
                "attribute_type_id": "translator:study_id",
                "value": int(study_id),
            }
        )
        attributes.append(
            {
                "attribute_type_id": "translator:internal_edge_id",
                "value": int(internal_id),
            }
        )

        edge_obj = {
            "id": edge_id,
            "subject": subj_id,
            "object": obj_id,
            "predicate": predicate,
            "attributes": attributes,
        }

        edges[edge_id] = edge_obj

    return {
        "nodes": nodes,
        "edges": edges,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Export comb_edge_node edges to NIH Translator DGX JSON."
    )
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--user", required=True)
    parser.add_argument("--password", required=True)
    parser.add_argument("--database", required=True)
    parser.add_argument("--study-id", type=int, required=True)
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Optional LIMIT on number of edges (default: no limit)",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Path to JSON output file (DGX format)",
    )

    args = parser.parse_args()

    try:
        conn = get_connection(
            host=args.host,
            user=args.user,
            password=args.password,
            database=args.database,
        )
    except Error as e:
        print(f"Error connecting to MySQL: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        rows = fetch_edges(conn, study_id=args.study_id, limit=args.limit)
        print(f"Fetched {len(rows)} rows for study_id={args.study_id}", file=sys.stderr)

        dgx_graph = build_dgx_graph(rows)

        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(dgx_graph, f, indent=2)

        print(f"Wrote DGX graph to {args.output}", file=sys.stderr)

    finally:
        conn.close()


if __name__ == "__main__":
    main()


