# nomad/normalizing/code_recommender.py

from nomad.normalizing.normalizer import Normalizer
from nomad.metainfo import Package, Quantity, Section, SubSection
from nomad.datamodel.metainfo.basesections import System
from .recommender_core import mapping_methods  # dein existierender Code

# Optional: Metainfo für deine Empfehlungen definieren
class CodeRecommendationSection(Section):
    recommended_code = Quantity(type=str, description='Empfohlener Code')
    matched_features = Quantity(type=str, shape=['*'], description='Getroffene Features')

class CodeRecommenderNormalizer(Normalizer):
    def normalize(self, archive, logger):
        # Beispiel: Methoden aus der Simulation auslesen
        # Hier brauchst du wahrscheinlich einen kontextabhängigen Zugriff
        try:
            method_list = archive.method[0].method_name  # musst ggf. anpassen
            logger.info(f'Empfehle Code für Methoden: {method_list}')
        except Exception:
            logger.warning('Keine method_list gefunden')
            return

        # Rufe deinen Recommender auf
        recommendations = mapping_methods(method_list)

        # Speichere Empfehlungen im Archive
        archive.m_add_sub_section(archive.workflow, CodeRecommendationSection())  # ggf. anpassen
        for rec in recommendations:
            section = CodeRecommendationSection()
            section.recommended_code = rec['code']
            section.matched_features = rec['methods']
            archive.m_add_sub_section('code_recommendation', section)
