"""
Project: Game of Papers
Group Members: Adit Negi, Jay Barot, Samir Gupta, Ryan Nachman
Date: 03/23/2022
"""

# import the necessary packages
import argparse
import logging
import torch
import json
# import hugging face transformers library
# provides interface to work with a wide range of pre-trained models
from transformers import AutoTokenizer, AutoModel
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import matplotlib.pyplot as plt


class BaseLineModelExperiments:
    
    def __init__(self, logger):
        self.tokenizer = None
        self.model = None
        self.input_data = None
        self.logger = logger


    def configure (self, args):
        try:  
            self.logger.info ("BaseLineModelExperiments::configure") 

            # load the tokenizer and model
            self.tokenizer = AutoTokenizer.from_pretrained(args.tokenizer)
            self.model = AutoModel.from_pretrained(args.model)

            # load the data
            self.input_data = self.load_data(args.input_data)

        except Exception as e:
            self.logger.error("Error while configuring the model: {}".format(e))
            raise e


    def driver(self):
        try:
            self.logger.info ("BaseLineModelExperiments::driver")

            # Tokenize the input data
            tokenized_sentences = self.tokenize()

            # Append the padding to the tokenized sentences
            input_sequence = self.append_padding(tokenized_sentences)
            
            # Run the model
            with torch.no_grad():
                # Get its last hidden state (the output of the last layer)
                embeddings = self.model(**input_sequence).last_hidden_state[:, 0, :]

            # Print the shape of the encoded outputs
            self.logger.info("Shape of the encoded outputs: {}".format(embeddings.shape))

            # Calculate cosine similarity between the embeddings
            similarity = cosine_similarity(embeddings.numpy())
            self.logger.info("Similarity matrix: \n {}".format(similarity))

            # Plot the similarity matrix
            # self.plot_similarity_matrix(similarity)

        except Exception as e:
            self.logger.error("Error while running the driver: {}".format(e))
            raise e


    """
    tokenize the input data
    """
    def tokenize(self):
        try:
            self.logger.info ("BaseLineModelExperiments::tokenize") 
            
            tokenized_sentences = []
            for sentence in self.input_data:
                tokenized_sentence = self.tokenizer(sentence['abstract'], padding=True, truncation=True, max_length=512)
                tokenized_sentence['id'] = sentence['id'] # add the id to the tokenized sentence
                tokenized_sentences.append(tokenized_sentence)
            
            return tokenized_sentences
            # return self.tokenizer([d["abstract"] for d in self.input_data], padding=True, truncation=True, return_tensors='pt')
        
        except Exception as e:
            self.logger.error("Error while tokenizing the input data: {}".format(e))
            raise e
    

    """
    This function appends the padding to the tokenized sentences

    :param tokenized_sentences: tokenized sentences
    :ptype tokenized_sentences: <list>
    :return: padded input ids and attention masks
    :rtype: <dict>
    """
    def append_padding(self, tokenized_sentences):
        try:
            self.logger.info ("BaseLineModelExperiments::append_padding") 

            # Get the maximum sequence length in the list of tokenized sentences
            max_len = max([len(sent['input_ids']) for sent in tokenized_sentences])

            # Create empty lists to store the padded input_ids and attention_masks
            padded_input_ids = []
            attention_masks = []

            # Loop through each sentence in the tokenized_sentences list
            for sent in tokenized_sentences:
                # Get the length of the input_ids for this sentence
                input_len = len(sent['input_ids'])
                
                # Pad the input_ids and attention_mask with zeros up to the max_len
                padded_input_ids.append(sent['input_ids'] + [0] * (max_len - input_len))
                attention_masks.append(sent['attention_mask'] + [0] * (max_len - input_len))
            
            # Convert the padded_input_ids and attention_masks to tensors
            padded_input_ids = torch.tensor(padded_input_ids)
            padded_attention_masks = torch.tensor(attention_masks)

            return {'input_ids': padded_input_ids, 'attention_mask': padded_attention_masks}
        
        except Exception as e:
            self.logger.error("Error while appending the padding to the tokenized sentences: {}".format(e))
            raise e
    

    """
    Load the data from the file

    :param file: file to load the data from
    :ptype file: str
    :return: data
    :rtype: <list>
    """
    def load_data(self, file):
        try:
            self.logger.info ("BaseLineModelExperiments::load_data") 

            # load the data
            with open(file, 'r') as f:
                data = json.loads( f.read() )
            
            f.close()

            return data
        
        except Exception as e:
            self.logger.error("Error while loading the data: {}".format(e))
            raise e
    

    """
    This function plots the similarity matrix
    
    :param similarity: similarity matrix
    :ptype similarity: <list>
    :param labels: labels for the similarity matrix
    :ptype labels: <list>
    """
    def plot_similarity_matrix(self, similarity, labels=None):
        try:
            fig, ax = plt.subplots(figsize=(6, 6))
            im = ax.imshow(similarity, cmap='YlOrRd', vmin=0, vmax=1)

            # Set axis labels and tick labels
            if labels is not None:
                ax.set_xticks(np.arange(len(labels)))
                ax.set_yticks(np.arange(len(labels)))
                ax.set_xticklabels(labels, rotation=45, ha="right")
                ax.set_yticklabels(labels)
            else:
                ax.set_xticks([])
                ax.set_yticks([])

            # Show the colorbar
            cbar = ax.figure.colorbar(im, ax=ax, fraction=0.046, pad=0.04)

            # Set the title and show the plot
            ax.set_title("Cosine Similarity Matrix")
            fig.tight_layout()
            plt.show()

        except Exception as e:
            self.logger.error("Error while plotting the similarity matrix: {}".format(e))
            raise e


def parseCmdLineArgs ():
    # instantiate a ArgumentParser object
    parser = argparse.ArgumentParser (description="CrossDocumentLanguageModel")

    parser.add_argument ("-l", "--loglevel", type=int, default=logging.INFO, choices=[logging.DEBUG,logging.INFO,logging.WARNING,logging.ERROR,logging.CRITICAL], help="logging level, choices 10,20,30,40,50: default 20=logging.INFO")

    parser.add_argument ("-t", "--tokenizer", default='biu-nlp/cdlm', help="Tokenizer, AutoTokenizer from hugging face hub, default:tokenizer = 'biu-nlp/cdlm' ")

    parser.add_argument ("-m", "--model", default='biu-nlp/cdlm', help="Model, AutoTokenizer from hugging face hub, default:model = 'biu-nlp/cdlm' ")

    parser.add_argument ("-i", "--input_data", default='sample.json', help="Input file, default:input = 'sample.json' ")

    return parser.parse_args()


"""
Main driver program
"""
def main():
    try:
        # obtain a system wide logger and initialize it to debug level to begin with
        logging.info ("Main - acquire a child logger and then log messages in the child")
        logger = logging.getLogger ("BaseLineModelExperiments")
        
        # first parse the arguments
        logger.debug ("Main: parse command line arguments")
        args = parseCmdLineArgs ()

        # reset the log level to as specified
        logger.debug ("Main: resetting log level to {}".format (args.loglevel))
        logger.setLevel (args.loglevel)
        logger.debug ("Main: effective log level is {}".format (logger.getEffectiveLevel ()))

        # Obtain a publisher application
        logger.debug ("Main: obtain the CDLM object")
        blme = BaseLineModelExperiments ( logger )

        # configure the object
        logger.debug ("Main: configure the publisher appln object")
        blme.configure (args)

        # now invoke the driver program
        logger.debug ("Main: invoke the publisher appln driver")
        blme.driver ()
        
    except Exception as e:
        logger.error ("Exception caught in main - {}".format (e))
        return


if __name__ == "__main__":
    # set underlying default logging capabilities
    logging.basicConfig (level=logging.DEBUG,
                       format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
  
    main()