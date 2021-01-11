"""
Tests for Text Classification Functionality
"""

from happytransformer.happy_text_classification import HappyTextClassification, TextClassificationResult

def test_classify_text():
    """
    Tests
    HappyQuestionAnswering.classify_text()

    """
    happy_tc = HappyTextClassification()
    result = happy_tc.classify_text("What a great movie")
    answer = TextClassificationResult(label='LABEL_1', score=0.9998726844787598)
    assert result == answer


def test_qa_train():
    """
    Tests
    HappyQuestionAnswering.train()

    """
    happy_tc = HappyTextClassification(model_type="DISTILBERT",
                 model_name="distilbert-base-uncased-finetuned-sst-2-english")

    happy_tc.train("../data/tc/train-eval.csv")


def test_qa_eval():
    """
    Tests
    HappyQuestionAnswering.eval()
    """
    happy_tc = HappyTextClassification(model_type="DISTILBERT",
                 model_name="distilbert-base-uncased-finetuned-sst-2-english")
    results = happy_tc.eval("../data/tc/train-eval.csv")
    assert results.eval_loss == 0.007262040860950947


def test_qa_test():
    """
    Tests
    HappyQuestionAnswering.test()
    """
    happy_tc = HappyTextClassification(model_type="DISTILBERT",
                 model_name="distilbert-base-uncased-finetuned-sst-2-english")

    result = happy_tc.test("../data/tc/test.csv")
    answer = [TextClassificationResult(label='LABEL_1', score=0.9998401999473572),
              TextClassificationResult(label='LABEL_0', score=0.9772131443023682),
              TextClassificationResult(label='LABEL_0', score=0.9966067671775818),
              TextClassificationResult(label='LABEL_1', score=0.9792295098304749)]
    assert result == answer


def test_qa_train_effectiveness():
    """
    Tests
    Ensures that HappyQuestionAnswering.train() results in
    lowering the loss as determined by HappyQuestionAnswering.eval()
    """

    happy_tc = HappyTextClassification(model_type="DISTILBERT",
                 model_name="distilbert-base-uncased-finetuned-sst-2-english")
    before_loss = happy_tc.eval("../data/tc/train-eval.csv").eval_loss
    happy_tc.train("../data/tc/train-eval.csv")
    after_loss = happy_tc.eval("../data/tc/train-eval.csv").eval_loss
    assert after_loss < before_loss



def test_qa_train_effectiveness_multi():
    """
    Tests
    Ensures that HappyQuestionAnswering.train() results in
    lowering the loss as determined by HappyQuestionAnswering.eval()
    """

    happy_tc = HappyTextClassification(model_type="DISTILBERT",
                 model_name="distilbert-base-uncased", num_labels=3)
    before_loss = happy_tc.eval("../data/tc/train-eval-multi.csv").eval_loss
    happy_tc.train("../data/tc/train-eval-multi.csv")
    after_loss = happy_tc.eval("../data/tc/train-eval-multi.csv").eval_loss
    assert after_loss < before_loss


def test_qa_test_multi_distil_bert():
    """
    Tests
    Ensures that HappyQuestionAnswering.train() results in
    lowering the loss as determined by HappyQuestionAnswering.eval()
    """

    happy_tc = HappyTextClassification(model_type="DISTILBERT",
                 model_name="distilbert-base-uncased", num_labels=3)
    happy_tc.train("../data/tc/train-eval-multi.csv")
    result = happy_tc.test("../data/tc/test-multi.csv")
    answer = [TextClassificationResult(label='LABEL_2', score=0.3558128774166107),
              TextClassificationResult(label='LABEL_2', score=0.34425610303878784),
              TextClassificationResult(label='LABEL_1', score=0.3998771607875824),
              TextClassificationResult(label='LABEL_1', score=0.38578158617019653),
              TextClassificationResult(label='LABEL_0', score=0.39120176434516907),
              TextClassificationResult(label='LABEL_0', score=0.3762877583503723)]
    assert result == answer


def test_qa_effectiveness_multi_albert():
    """
    Tests
    Ensures that HappyQuestionAnswering.train() results in
    lowering the loss as determined by HappyQuestionAnswering.eval()
    """

    happy_tc = HappyTextClassification(model_type="ALBERT",
                 model_name="albert-base-v2", num_labels=3)
    before_loss = happy_tc.eval("../data/tc/train-eval-multi.csv").eval_loss
    happy_tc.train("../data/tc/train-eval-multi.csv")
    after_loss = happy_tc.eval("../data/tc/train-eval-multi.csv").eval_loss
    assert after_loss < before_loss

def test_qa_effectiveness_multi_bert():
    """
    Tests
    Ensures that HappyQuestionAnswering.train() results in
    lowering the loss as determined by HappyQuestionAnswering.eval()
    """

    happy_tc = HappyTextClassification(model_type="BERT",
                 model_name="bert-base-uncased", num_labels=3)
    before_loss = happy_tc.eval("../data/tc/train-eval-multi.csv").eval_loss
    happy_tc.train("../data/tc/train-eval-multi.csv")
    after_loss = happy_tc.eval("../data/tc/train-eval-multi.csv").eval_loss
    assert after_loss < before_loss


def test_qa_test_albert():
    """
    Tests
    HappyQuestionAnswering.test()
    """
    happy_tc = HappyTextClassification(model_type="ALBERT", model_name="textattack/albert-base-v2-SST-2")

    result = happy_tc.test("../data/tc/test.csv")
    answer = [TextClassificationResult(label='LABEL_1', score=0.9990348815917969),
              TextClassificationResult(label='LABEL_0', score=0.9947203397750854),
              TextClassificationResult(label='LABEL_0', score=0.9958302974700928),
              TextClassificationResult(label='LABEL_1', score=0.9986426830291748)]
    assert result == answer


def test_qa_train_effectiveness_albert():
    """
    Tests
    Ensures that HappyQuestionAnswering.train() results in
    lowering the loss as determined by HappyQuestionAnswering.eval()
    """

    happy_tc = HappyTextClassification(model_type="ALBERT", model_name="textattack/albert-base-v2-SST-2")
    before_loss = happy_tc.eval("../data/tc/train-eval.csv").eval_loss
    happy_tc.train("../data/tc/train-eval.csv")
    after_loss = happy_tc.eval("../data/tc/train-eval.csv").eval_loss
    assert after_loss < before_loss


def test_qa_test_bert():
    """
    Tests
    HappyQuestionAnswering.test()
    """
    happy_tc = HappyTextClassification(model_type="BERT", model_name="textattack/bert-base-uncased-SST-2")

    result = happy_tc.test("../data/tc/test.csv")
    answer = [TextClassificationResult(label='LABEL_1', score=0.9995690584182739),
              TextClassificationResult(label='LABEL_0', score=0.9981549382209778),
              TextClassificationResult(label='LABEL_0', score=0.9965545535087585),
              TextClassificationResult(label='LABEL_1', score=0.9978235363960266)]
    assert result == answer


def test_qa_train_effectiveness_bert():
    """
    Tests
    Ensures that HappyQuestionAnswering.train() results in
    lowering the loss as determined by HappyQuestionAnswering.eval()
    """

    happy_tc = HappyTextClassification(model_type="BERT", model_name="textattack/bert-base-uncased-SST-2")
    before_loss = happy_tc.eval("../data/tc/train-eval.csv").eval_loss
    happy_tc.train("../data/tc/train-eval.csv")
    after_loss = happy_tc.eval("../data/tc/train-eval.csv").eval_loss
    assert after_loss < before_loss
