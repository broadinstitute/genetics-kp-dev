
"""
Export MySQL comb_edge_node data to KGX TSV (TRAPI 1.4 / Biolink-conformant).

This will write:
  magma_alz_nodes.tsv
  magma_alz_edges.tsv
"""

# imports
import sys
import csv
from typing import Dict, Any, List, Tuple, Set
import os

import pymysql
from pymysql.cursors import DictCursor

# constants
DB_PASSWD = os.environ.get('DB_PASSWD')
DB_SCHEMA = 'tran_test_202303'
DIR_KGX = "/Users/mduby/Data/Broad/Translator/GeneticsPro/KGX"

DB_STUDY_ID = 1
INFORES_GENETICS = "infores:genetics-data-provider"

# These defaults reflect MAGMA-style statistical associations
DEFAULT_KNOWLEDGE_LEVEL = "statistical_association"
DEFAULT_AGENT_TYPE = "data_analysis_pipeline"


# ---------------------------------------------------------------------
# DB access
# ---------------------------------------------------------------------

def get_connection(host: str, user: str, password: str, database: str):
    return pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=database,
        cursorclass=DictCursor,
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
        LIMIT 10
    """
    if limit is not None and limit > 0:
        query += " LIMIT %s"

    cursor = conn.cursor()
    try:
        if limit is not None and limit > 0:
            cursor.execute(query, (study_id, limit))
        else:
            cursor.execute(query, (study_id,))
        rows = cursor.fetchall()
        return rows
    finally:
        cursor.close()


# ---------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------

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

    if "," in text:
        parts = [p.strip() for p in text.split(",")]
    elif ";" in text:
        parts = [p.strip() for p in text.split(";")]
    else:
        parts = [text]

    return [p for p in parts if p]


def list_to_pipe(values: List[str]) -> str:
    """
    KGX TSV uses '|' for multivalued columns.
    """
    return "|".join(str(v) for v in values) if values else ""


# ---------------------------------------------------------------------
# KGX building
# ---------------------------------------------------------------------

def build_kgx(
    rows: List[Dict[str, Any]],
    kp_infores: str,
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Build KGX-style node and edge records from DB rows.

    Returns:
      (node_records, edge_records)
    """
    # node_id -> node dict
    nodes: Dict[str, Dict[str, Any]] = {}
    edges: List[Dict[str, Any]] = []

    for row in rows:
        edge_id = row["edge_id"]
        subj_id = row["subject_id"]
        obj_id = row["object_id"]

        subj_name = row["subject_name"]
        obj_name = row["object_name"]

        subj_cat = row["subject_category"]  # e.g. "biolink:Gene"
        obj_cat = row["object_category"]    # e.g. "biolink:Disease"

        predicate = row["predicate"]        # e.g. "biolink:gene_associated_with_condition"

        score = row["score"]
        score_type = row["score_type"]      # e.g. "p_value"
        score_translator = row["score_translator"]
        study_id = row["study_id"]
        internal_id = row["internal_id"]

        pub_ids_list = parse_publication_ids(row["publication_ids"])

        # ------------------------
        # Nodes (KGX node records)
        # Required: id, category
        # Example TSV header: id  category  name  provided_by
        # ------------------------

        if subj_id not in nodes:
            nodes[subj_id] = {
                "id": subj_id,
                "name": subj_name or "",
                # category is multivalued in KGX; here it's a single label or pipe-delimited string
                "category": subj_cat if subj_cat else "",
                # 'provided_by' is node-only provenance in KGX spec
                "provided_by": kp_infores,
            }

        if obj_id not in nodes:
            nodes[obj_id] = {
                "id": obj_id,
                "name": obj_name or "",
                "category": obj_cat if obj_cat else "",
                "provided_by": kp_infores,
            }

        # ------------------------
        # Edge (KGX edge record)
        #
        # Required properties (per spec):
        #   subject, predicate, object, knowledge_level, agent_type
        #
        # TSV example header:
        #   id  subject  predicate  object  relation  primary_knowledge_source  category  publications
        #
        # NOTE:
        # - 'relation' is deprecated but still allowed; we leave it blank.
        # - 'provided_by' is node-only; for edges we use knowledge_source properties.
        # ------------------------

        edge_rec: Dict[str, Any] = {
            "id": edge_id,
            "subject": subj_id,
            "predicate": predicate,
            "object": obj_id,
            # Biolink "relation" (often a lower-level RO term); optional & deprecated
            "relation": "",
            # Association category; could be made more specific if desired
            "category": "biolink:Association",
            # KGX / Biolink edge provenance
            "primary_knowledge_source": kp_infores,
            # leave aggregator blank unless you have one
            "aggregator_knowledge_source": "",
            # Required KGX/Biolink edge metadata
            "knowledge_level": DEFAULT_KNOWLEDGE_LEVEL,
            "agent_type": DEFAULT_AGENT_TYPE,
        }

        # Score as extra edge properties
        if score is not None:
            edge_rec["score"] = float(score)
            edge_rec["score_type"] = score_type or ""

        if score_translator is not None:
            edge_rec["score_translator"] = float(score_translator)

        if pub_ids_list:
            # Multivalued KGX column, pipe-delimited
            edge_rec["publications"] = list_to_pipe(pub_ids_list)

        edge_rec["study_id"] = int(study_id)
        edge_rec["internal_edge_id"] = int(internal_id)

        edges.append(edge_rec)

    # Return flat lists of dicts
    node_records = list(nodes.values())
    edge_records = edges
    return node_records, edge_records


# ---------------------------------------------------------------------
# File writing
# ---------------------------------------------------------------------

def write_nodes_tsv(path: str, nodes: List[Dict[str, Any]]):
    """
    Write nodes in KGX TSV format.

    We'll include common columns:
      id, category, name, provided_by
    plus any extra keys seen in the nodes.
    """
    # Collect all keys
    all_keys: Set[str] = set()
    for n in nodes:
        all_keys.update(n.keys())

    # Default core node columns (ordered like KGX TSV example)
    core = ["id", "category", "name", "description", "xref", "provided_by", "synonym"]

    # Build header in KGX-like order
    header: List[str] = []
    for c in core:
        if c in all_keys:
            header.append(c)
            all_keys.remove(c)
    # remaining, sorted
    for k in sorted(all_keys):
        header.append(k)

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=header, delimiter="\t", quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        for n in nodes:
            writer.writerow({k: n.get(k, "") for k in header})


def write_edges_tsv(path: str, edges: List[Dict[str, Any]]):
    """
    Write edges in KGX TSV format.

    Core edge columns (per spec + example):
      id, subject, predicate, object, relation,
      primary_knowledge_source, aggregator_knowledge_source,
      category, publications, knowledge_level, agent_type

    Additional keys (score, study_id, etc.) are appended afterward.
    """
    all_keys: Set[str] = set()
    for e in edges:
        all_keys.update(e.keys())

    core = [
        "id",
        "subject",
        "predicate",
        "object",
        "relation",
        "primary_knowledge_source",
        "aggregator_knowledge_source",
        "category",
        "publications",
        "knowledge_level",
        "agent_type",
    ]

    header: List[str] = []
    for c in core:
        if c in all_keys:
            header.append(c)
            all_keys.remove(c)
    for k in sorted(all_keys):
        header.append(k)

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=header, delimiter="\t", quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        for e in edges:
            writer.writerow({k: e.get(k, "") for k in header})


# ---------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------

def main():
    try:
        conn = get_connection(
            host='localhost',
            user='root',
            password=DB_PASSWD,
            database=DB_SCHEMA,
        )

    except pymysql.MySQLError as e:
        print(f"Error connecting to MySQL: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        rows = fetch_edges(conn, study_id=DB_STUDY_ID)
        print(f"Fetched {len(rows)} rows for study_id={DB_STUDY_ID}", file=sys.stderr)

        node_records, edge_records = build_kgx(rows, kp_infores=INFORES_GENETICS)

        nodes_path = f"{DIR_KGX}/nodes_geneticsKP_magma.json"
        edges_path = f"{DIR_KGX}/edges_geneticsKP_magma.json"

        write_nodes_tsv(nodes_path, node_records)
        write_edges_tsv(edges_path, edge_records)

        print(f"Wrote KGX nodes to {nodes_path}", file=sys.stderr)
        print(f"Wrote KGX edges to {edges_path}", file=sys.stderr)

    finally:
        conn.close()


if __name__ == "__main__":
    main()
