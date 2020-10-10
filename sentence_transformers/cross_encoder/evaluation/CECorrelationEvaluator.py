import logging
from scipy.stats import pearsonr, spearmanr
from typing import List
from ... import InputExample

class CECorrelationEvaluator:
    """
    This evaluator can be used with the CrossEncoder class. Given sentence pairs and continuous scores,
    it compute the pearson & spearman correlation between the predicted score for the sentence pair
    and the gold score.
    """
    def __init__(self, sentence_pairs: List[List[str]], scores: List[float], name: str=''):
        self.sentence_pairs = sentence_pairs
        self.scores = scores
        self.name = name

    @classmethod
    def from_input_examples(cls, examples: List[InputExample], **kwargs):
        sentence_pairs = []
        scores = []

        for example in examples:
            sentence_pairs.append(example.texts)
            scores.append(example.label)
        return cls(sentence_pairs, scores, **kwargs)

    def __call__(self, model, output_path: str = None, epoch: int = -1, steps: int = -1) -> float:
        if epoch != -1:
            if steps == -1:
                out_txt = " after epoch {}:".format(epoch)
            else:
                out_txt = " in epoch {} after {} steps:".format(epoch, steps)
        else:
            out_txt = ":"

        logging.info("CECorrelationEvaluator: Evaluating the model on " + self.name + " dataset" + out_txt)
        pred_scores = model.predict(self.sentence_pairs, convert_to_numpy=True, show_progress_bar=False)


        eval_pearson, _ = pearsonr(self.scores, pred_scores)
        eval_spearman, _ = spearmanr(self.scores, pred_scores)

        logging.info("Correlation:\tPearson: {:.4f}\tSpearman: {:.4f}".format(eval_pearson, eval_spearman))

        return eval_spearman