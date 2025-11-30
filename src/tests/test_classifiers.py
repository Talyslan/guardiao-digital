from src.infra.classifiers.rule_based_classifier import RuleBasedClassifier

def test_rule_based_basic():
    rc = RuleBasedClassifier()
    assert rc.classify("Você ganhou um prêmio! Clique aqui") >= 0.7
    assert rc.classify("Reunião amanhã às 10h") < 0.3
