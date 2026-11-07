"""
Generació de microconsultes i publicació simulada.

La generació és determinista i basada en plantilles: a la demo no cal un LLM
per demostrar el flux, i així l'equip pot explicar exactament per què la IA
proposa cada pregunta. A `docs/CONTRATO_API.md` es descriu com substituir-ho
per una crida real a un model.
"""

from __future__ import annotations

import hashlib
import io
import random
from datetime import datetime

import qrcode

TIPUS_ESCALA = "Escala 1-5"
TIPUS_OPCIONS = "Opcions múltiples"
TIPUS_SI_NO = "Sí/No"
TIPUS_OBERT = "Text obert"

TEMES_PROHIBITS_CLAU = {
    "salari": ["salari", "sou", "retribucio", "compensacio", "bonus"],
    "salut": ["salut", "malaltia", "baixa medica", "medic"],
    "torns": ["torn", "horari"],
    "lideratge": ["cap", "lider", "manager"],
    "conciliacio": ["conciliacio", "familia"],
    "formacio": ["formacio", "curs"],
    "eines": ["eina", "sistema", "aplicacio"],
}

# Preguntes per tema: (escala, oberta, opcions múltiples)
BANC_PREGUNTES = {
    "Torns i horaris": {
        "escala": "Com valores la planificació dels teus torns aquest mes?",
        "oberta": "Quin canvi concret en els torns t'ajudaria més?",
        "opcions": (
            "Quin és el principal problema dels torns?",
            ["Poca antelació", "Rotació poc saludable", "Canvis d'última hora", "Falta de flexibilitat"],
        ),
    },
    "Descansos i pauses": {
        "escala": "Pots fer les pauses que et corresponen en un dia normal?",
        "oberta": "Què et caldria per poder descansar de veritat durant la jornada?",
        "opcions": (
            "Què dificulta més les pauses?",
            ["Falta de relleu", "Pic de feina", "Espais inadequats", "Cultura d'equip"],
        ),
    },
    "Càrrega de treball": {
        "escala": "Com valores el volum de feina de les últimes setmanes?",
        "oberta": "Quina part de la teva càrrega es podria reduir o repartir millor?",
        "opcions": (
            "On es nota més la sobrecàrrega?",
            ["Pics de producció", "Baixes no cobertes", "Tasques administratives", "Reunions"],
        ),
    },
    "Comunicació": {
        "escala": "La informació que reps sobre els canvis arriba a temps i és clara?",
        "oberta": "Quin canal o format t'ajudaria a estar millor informat/da?",
        "opcions": (
            "Quin és el principal buit de comunicació?",
            ["No s'explica el perquè", "Arriba tard", "Massa canals diferents", "No arriba a planta"],
        ),
    },
    "Lideratge": {
        "escala": "El teu responsable directe et dona feedback útil i freqüent?",
        "oberta": "Què faria més útil l'acompanyament del teu responsable?",
        "opcions": (
            "Quin aspecte del lideratge caldria reforçar?",
            ["Feedback", "Autonomia", "Claredat d'objectius", "Gestió de conflictes"],
        ),
    },
    "Reconeixement": {
        "escala": "Sents que la teva feina es reconeix quan està ben feta?",
        "oberta": "Quin tipus de reconeixement seria significatiu per a tu?",
        "opcions": (
            "On falta més reconeixement?",
            ["Equip", "Persones", "Projectes", "Esforç extra"],
        ),
    },
    "Conciliació": {
        "escala": "Pots conciliar la teva vida personal amb l'horari actual?",
        "oberta": "Quina mesura de flexibilitat marcaria la diferència?",
        "opcions": (
            "Què limita més la conciliació?",
            ["Horari de tancament", "Canvis d'última hora", "Càrrega", "Criteris poc clars"],
        ),
    },
    "Formació i desenvolupament": {
        "escala": "La formació que reps s'aplica al teu dia a dia?",
        "oberta": "Què t'agradaria aprendre els pròxims sis mesos?",
        "opcions": (
            "Què caldria millorar de la formació?",
            ["Més temps", "Més pràctica", "Pla de carrera clar", "Cursos per col·lectiu"],
        ),
    },
    "Eines i processos": {
        "escala": "Les eines i processos et permeten fer la feina sense fricció?",
        "oberta": "Quin procés simplificaries demà mateix?",
        "opcions": (
            "On hi ha més fricció?",
            ["Eines poc integrades", "Massa passes", "Falta de formació", "Sistemes lents"],
        ),
    },
    "Salut i seguretat": {
        "escala": "Et sents segur/da en el teu lloc de treball?",
        "oberta": "Quina millora de seguretat o ergonomia és més urgent?",
        "opcions": (
            "Quin risc et preocupa més?",
            ["Postura", "Soroll", "Càrrega física", "Equips de protecció"],
        ),
    },
    "Ambient i relacions": {
        "escala": "Com valores l'ambient de treball del teu equip?",
        "oberta": "Què ajudaria a millorar la col·laboració entre torns o equips?",
        "opcions": (
            "On caldria posar més atenció?",
            ["Coordinació entre torns", "Respecte", "Suport entre companys", "Comunicació informal"],
        ),
    },
    "Organització i recursos": {
        "escala": "Els recursos i l'organització del teu equip són suficients?",
        "oberta": "Quin recurs o decisió organitzativa canviaries?",
        "opcions": (
            "Què falta més?",
            ["Plantilla", "Planificació", "Estructura clara", "Informació de decisions"],
        ),
    },
}

COL_LECTIU_TEMES = {
    "Planta": ["Torns i horaris", "Descansos i pauses", "Càrrega de treball", "Salut i seguretat", "Comunicació"],
    "Logística": ["Càrrega de treball", "Torns i horaris", "Eines i processos", "Descansos i pauses", "Comunicació"],
    "Comercial": ["Conciliació", "Càrrega de treball", "Reconeixement", "Comunicació", "Eines i processos"],
    "Oficina": ["Lideratge", "Comunicació", "Conciliació", "Formació i desenvolupament", "Reconeixement"],
    "Manager": ["Lideratge", "Organització i recursos", "Comunicació", "Formació i desenvolupament", "Càrrega de treball"],
}

INTROS = {
    "Proper i directe": "Volem saber com ho estàs vivint de veritat. Són unes preguntes curtes, anònimes i pensades per actuar, no per avaluar persones.",
    "Neutre i formal": "Aquesta microconsulta té com a objectiu conèixer la percepció del col·lectiu sobre els aspectes següents. Les respostes són anònimes i s'analitzaran de forma agregada.",
    "Motivador": "La teva opinió compte i molt. Amb menys de dos minuts ens ajudes a prendre millors decisions per al teu equip.",
}


def _detecta_temes_objectiu(objectiu: str) -> list[str]:
    objectiu_net = objectiu.lower()
    trobats = []
    for tema, claus in {
        "Torns i horaris": ["torn", "horari", "rotacio"],
        "Descansos i pauses": ["descans", "pausa"],
        "Càrrega de treball": ["carrega", "volum", "feina", "estres"],
        "Comunicació": ["comunicacio", "informacio", "canal"],
        "Lideratge": ["lider", "cap", "feedback"],
        "Reconeixement": ["reconeix", "valorar"],
        "Conciliació": ["concili", "familia", "flexibilitat"],
        "Formació i desenvolupament": ["formacio", "curs", "aprendre", "carrera"],
        "Eines i processos": ["eina", "sistema", "proces", "aplicacio"],
        "Salut i seguretat": ["salut", "seguretat", "ergonomia", "risc"],
        "Ambient i relacions": ["ambient", "equip", "relacio"],
        "Organització i recursos": ["organitzacio", "recursos", "plantilla"],
    }.items():
        if any(c in objectiu_net for c in claus):
            trobats.append(tema)
    return trobats


def _esta_prohibit(tema: str, prohibits: list[str]) -> bool:
    tema_net = tema.lower()
    for p in prohibits:
        claus = TEMES_PROHIBITS_CLAU.get(p.lower(), [p.lower()])
        if any(c in tema_net for c in claus):
            return True
    return False


def _tria_temes(necessitat: dict, rng: random.Random) -> list[str]:
    col = necessitat.get("col_lectiu", "Oficina")
    prohibits = necessitat.get("temes_prohibits", [])
    candidats = _detecta_temes_objectiu(necessitat.get("objectiu", ""))
    for tema in COL_LECTIU_TEMES.get(col, []):
        if tema not in candidats:
            candidats.append(tema)
    candidats = [t for t in candidats if not _esta_prohibit(t, prohibits)]
    # Manté l'ordre però amb una mica de variació per semblar una proposta nova.
    if len(candidats) > 4:
        caps = candidats[:2]
        resta = candidats[2:]
        rng.shuffle(resta)
        candidats = caps + resta
    return candidats[:4]


def generar_consulta(necessitat: dict, variacio: int = 0) -> dict:
    """Genera una proposta de microconsulta a partir de la necessitat de RRHH."""
    llavor = hashlib.md5(
        (necessitat.get("objectiu", "") + necessitat.get("col_lectiu", "") + str(variacio)).encode("utf-8")
    ).hexdigest()
    rng = random.Random(int(llavor[:8], 16))

    col = necessitat.get("col_lectiu", "Oficina")
    to = necessitat.get("to", "Proper i directe")
    max_minuts = int(necessitat.get("durada_max", 2))
    temes = _tria_temes(necessitat, rng)
    context = necessitat.get("context", "").strip()

    titol_base = {
        "Torns i horaris": "Com vius els torns?",
        "Descansos i pauses": "Pauses reals, equips millors",
        "Càrrega de treball": "Com va la càrrega?",
        "Comunicació": "T'arriba la informació?",
        "Lideratge": "Com t'acompanya el teu responsable?",
        "Reconeixement": "Es reconeix la teva feina?",
        "Conciliació": "Conciliar és possible?",
        "Formació i desenvolupament": "Cap on vols créixer?",
        "Eines i processos": "Eines que ajuden o destorben?",
        "Salut i seguretat": "Com et sents de segur/da?",
        "Ambient i relacions": "Com és l'ambient del teu equip?",
        "Organització i recursos": "Tenim els recursos que calen?",
    }
    tema_principal = temes[0] if temes else "Comunicació"
    titol = titol_base.get(tema_principal, "Com ho estàs vivint?")
    if context:
        titol = f"{titol} · {context[:38]}"

    intro = INTROS[to]
    intro += (
        f" Aquesta consulta és per al col·lectiu {col.lower()} i estarà oberta "
        f"uns quants dies. Els resultats es mostraran sempre de forma agregada."
    )

    preguntes: list[dict] = []
    # 1. Pregunta comuna de benestar.
    preguntes.append(
        {
            "id": "q1",
            "text": "Com et sents de benestar general a la feina aquestes últimes setmanes?",
            "tipus": TIPUS_ESCALA,
            "opcions": [],
            "obligatoria": True,
            "condicional": "",
        }
    )

    # 2-4. Preguntes del temari específic.
    for tema in temes[:3]:
        banc = BANC_PREGUNTES.get(tema)
        if not banc:
            continue
        tipus_tria = ["escala", "opcions", "oberta"]
        rng.shuffle(tipus_tria)
        for tipus in tipus_tria[:2]:
            if tipus == "escala":
                preguntes.append(
                    {
                        "id": f"q{len(preguntes) + 1}",
                        "text": banc["escala"],
                        "tipus": TIPUS_ESCALA,
                        "opcions": [],
                        "obligatoria": True,
                        "condicional": "",
                    }
                )
            elif tipus == "opcions":
                text, opcions = banc["opcions"]
                preguntes.append(
                    {
                        "id": f"q{len(preguntes) + 1}",
                        "text": text,
                        "tipus": TIPUS_OPCIONS,
                        "opcions": opcions,
                        "obligatoria": True,
                        "condicional": "",
                    }
                )
            else:
                preguntes.append(
                    {
                        "id": f"q{len(preguntes) + 1}",
                        "text": banc["oberta"],
                        "tipus": TIPUS_OBERT,
                        "opcions": [],
                        "obligatoria": False,
                        "condicional": "",
                    }
                )

    # 5. Pregunta oberta de tancament.
    if temes:
        banc = BANC_PREGUNTES.get(temes[0], {})
        if banc.get("oberta") and not any(p["text"] == banc["oberta"] for p in preguntes):
            preguntes.append(
                {
                    "id": f"q{len(preguntes) + 1}",
                    "text": banc["oberta"],
                    "tipus": TIPUS_OBERT,
                    "opcions": [],
                    "obligatoria": False,
                    "condicional": "",
                }
            )

    # Lògica condicional: si la primera escala és baixa, pregunta què ho explica.
    if len(preguntes) >= 2:
        seguiment = {
            "id": f"q{len(preguntes) + 1}",
            "text": "Què és el que més t'ho dificulta ara mateix?",
            "tipus": TIPUS_OBERT,
            "opcions": [],
            "obligatoria": False,
            "condicional": "Es mostra només si la pregunta 1 es respon amb 1 o 2.",
        }
        preguntes.append(seguiment)

    # Ajusta el nombre de preguntes a la durada màxima (≈20 s per pregunta).
    max_preguntes = max(3, min(6, max_minuts * 3))
    preguntes = preguntes[:max_preguntes]

    for i, p in enumerate(preguntes, start=1):
        p["id"] = f"q{i}"

    segons = 0
    for p in preguntes:
        segons += {TIPUS_ESCALA: 12, TIPUS_OPCIONS: 15, TIPUS_SI_NO: 10, TIPUS_OBERT: 35}.get(p["tipus"], 20)
    temps_estimat = max(1, round(segons / 60))

    return {
        "id": f"consulta-{llavor[:6]}",
        "creada": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "estat": "Esborrany",
        "titol": titol,
        "intro": intro,
        "to": to,
        "col_lectiu": col,
        "objectiu": necessitat.get("objectiu", ""),
        "context": context,
        "durada_max": max_minuts,
        "temps_estimat": temps_estimat,
        "canal": necessitat.get("canal", "Mòbil-QR"),
        "temes": temes,
        "preguntes": preguntes,
        "logica": [p["condicional"] for p in preguntes if p["condicional"]],
        "enllac": "",
        "qr": b"",
        "publicada_el": "",
    }


def publica_consulta(consulta: dict) -> dict:
    """Simula la publicació via API i genera enllaç + QR."""
    codi = consulta["id"].split("-")[-1].upper()
    enllac = f"https://form.typeform.com/to/damm-{codi}"
    img = qrcode.make(enllac)
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    consulta = dict(consulta)
    consulta.update(
        {
            "estat": "Publicada",
            "enllac": enllac,
            "qr": buffer.getvalue(),
            "publicada_el": datetime.now().strftime("%d/%m/%Y %H:%M"),
        }
    )
    return consulta
