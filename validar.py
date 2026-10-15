"""Valida interações e ativos gerados contra os JSON Schemas do CommunityLab.

Uso:
    python validar.py data/samples/cenarios_demo.json
    python validar.py

Requer: pip install jsonschema
"""
import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

BASE = Path(__file__).parent
SCHEMA_INTERACAO = json.loads((BASE / "schemas/interacao_schema.json").read_text(encoding="utf-8"))
SCHEMA_ATIVO = json.loads((BASE / "schemas/ativo_gerado_schema.json").read_text(encoding="utf-8"))

val_interacao = Draft202012Validator(SCHEMA_INTERACAO, format_checker=FormatChecker())
val_ativo = Draft202012Validator(SCHEMA_ATIVO, format_checker=FormatChecker())


def erros(validador, item):
    return [f"{'/'.join(map(str, e.path)) or '(raiz)'}: {e.message}" for e in validador.iter_errors(item)]


def validar_cenario(cenario):
    problemas = []
    ids = [i.get("id") for i in cenario["interacoes"]]
    if len(ids) != len(set(ids)):
        problemas.append("ids de interação duplicados")

    for i in cenario["interacoes"]:
        for e in erros(val_interacao, i):
            problemas.append(f"interacao {i.get('id')}: {e}")

    for a in cenario["ativos"]:
        for e in erros(val_ativo, a):
            problemas.append(f"ativo {a.get('id_ativo')}: {e}")
        for ref in a.get("interacoes_origem", []):
            if ref not in ids:
                problemas.append(f"ativo {a.get('id_ativo')}: interacoes_origem aponta para id inexistente ({ref})")
    return problemas


def main(caminho):
    p = Path(caminho)
    # Suporte a migração: se apontar para schemas/cenarios_demo.json, redireciona para data/samples/
    if not p.exists() and "schemas" in str(p):
        tentativa = BASE / "data/samples" / p.name
        if tentativa.exists():
            p = tentativa
    if not p.exists():
        sys.exit(f"Arquivo não encontrado: {caminho}")

    dados = json.loads(p.read_text(encoding="utf-8"))
    total = 0
    for c in dados["cenarios"]:
        problemas = validar_cenario(c)
        total += len(problemas)
        status = "OK" if not problemas else f"{len(problemas)} problema(s)"
        print(f"[{c['id']}] {c['titulo']}: {status}")
        for prob in problemas:
            print(f"   - {prob}")
    sys.exit(1 if total else 0)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        padrao = BASE / "data/samples/cenarios_demo.json"
        if padrao.exists():
            main(str(padrao))
        else:
            sys.exit("Uso: python validar.py <arquivo.json>")
    elif len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        sys.exit("Uso: python validar.py <arquivo.json>")
