"""
Fine-tuning for masked word prediction models.

Based on the tutorial found here:
https://github.com/huggingface/transformers/blob/master/examples/pytorch/language-modeling/run_mlm.py
"""
from dataclasses import dataclass
from transformers import DataCollatorForLanguageModeling
from happytransformer.happy_trainer import HappyTrainer, EvalResult
from datasets import load_dataset
from happytransformer.fine_tuning_util import preprocess_concatenate
import json

@dataclass
class WPTrainArgs:
    learning_rate: float
    weight_decay: float
    adam_beta1: float
    adam_beta2: float
    adam_epsilon: float
    max_grad_norm:  float
    num_train_epochs: int
    preprocessing_processes: int
    mlm_probability: float
    line_by_line: bool
    save_preprocessed_data: False
    save_preprocessed_data_path: ""
    load_preprocessed_data: False
    load_preprocessed_data_path: ""


@dataclass
class WPEvalArgs:
    preprocessing_processes: int
    mlm_probability: float
    line_by_line: bool
    save_preprocessed_data: False
    save_preprocessed_data_path: ""
    load_preprocessed_data: False
    load_preprocessed_data_path: ""



class WPTrainer(HappyTrainer):
    """
    Trainer class for HappyWordPrediction
    """
    def train(self, input_filepath, dataclass_args: WPTrainArgs):
        if not dataclass_args.load_preprocessed_data:
            self.logger.info("Preprocessing dataset...")

            dataset = load_dataset("text", data_files={"train": input_filepath})
            if dataclass_args.line_by_line:
                tokenized_dataset = self._preprocess_line_by_line(self.tokenizer, dataset, dataclass_args.preprocessing_processes)
            else:
                tokenized_dataset = preprocess_concatenate(self.tokenizer, dataset, dataclass_args.preprocessing_processes, True)
        else:
            self.logger.info("Loading dataset from %s...", dataclass_args.load_preprocessed_data_path)
            tokenized_dataset = load_dataset("json", data_files={"train": dataclass_args.load_preprocessed_data_path}, field='train')

        if dataclass_args.save_preprocessed_data:
            if dataclass_args.load_preprocessed_data:
                self.logger.warning("Both save_preprocessed_data and load_data are enabled,")

            self.logger.info("Saving training dataset to %s...", dataclass_args.save_preprocessed_data_path)

            self._generate_json(dataclass_args.save_preprocessed_data_path, tokenized_dataset["train"], "train")

        data_collator = DataCollatorForLanguageModeling(tokenizer=self.tokenizer,
                                                        mlm_probability=dataclass_args.mlm_probability)
        self.logger.info("Training...")

        self._run_train(tokenized_dataset['train'], dataclass_args, data_collator)


    def eval(self, input_filepath, dataclass_args: WPEvalArgs):
        dataset = load_dataset("text", data_files={"eval": input_filepath})

        if dataclass_args.line_by_line:
            tokenized_dataset = self._preprocess_line_by_line(self.tokenizer, dataset, dataclass_args.preprocessing_processes)
        else:
            tokenized_dataset = preprocess_concatenate(self.tokenizer, dataset, dataclass_args.preprocessing_processes, True)


        data_collator = DataCollatorForLanguageModeling(tokenizer=self.tokenizer,
                                                        mlm_probability=dataclass_args.mlm_probability)
        result = self._run_eval(tokenized_dataset['eval'], data_collator)

        return EvalResult(loss=result["eval_loss"])


    def test(self, input_filepath, solve, args):
        raise NotImplementedError()


    def _preprocess_line_by_line(self, tokenizer, dataset, preprocessing_processes):
        """
        :param tokenizer: tokenizer for a transformer model
        :param datasets: a datasets.Dataset object
        :param preprocessing_processes: number of processes to use for pre-processing
        :return:
        """

        def tokenize_function(example):
            return tokenizer(example["text"],
                             add_special_tokens=True, truncation=True,)

        tokenized_dataset = dataset.map(tokenize_function, batched=True,
                                          num_proc=preprocessing_processes,
                                          remove_columns=["text"])
        return tokenized_dataset


    def _generate_json(self, json_path, dataset, name):
        data = {}
        data[name] = []
        data = {
            name: [
                {
                    'attention_mask': case['attention_mask'],
                    'input_ids': case['input_ids'],
                }
                for case in dataset
            ]
        }

        with open(json_path, 'w') as outfile:
            json.dump(data, outfile)