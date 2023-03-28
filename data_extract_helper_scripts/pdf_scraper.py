"""
Project: Game of Papers
Group Members: Adit Negi, Jay Barot, Samir Gupta, Ryan Nachman
Date: 03/27/2022
"""

# import the necessary packages
import fitz
import logging
import argparse
import os
import json


class PdfScraper:


    def __init__(self, logger):
        self.script_dir = None # path of the directory containing the Python script
        self.input_data_dir = None # path of the directory containing the input data
        self.output = None # output data
        self.output_file = None # output file
        self.output_text_translations = None # boolean flag to indicate whether to output the text translations
        self.logger = logger
    

    def configure (self, args):
        try:  
            self.logger.info ("PdfScraper::configure") 
            # get the path of the directory containing the Python script
            self.script_dir = os.path.dirname(os.path.abspath(__file__))

            # get the path of the directory containing the input data
            self.input_data_dir = os.path.join(self.script_dir, args.input_data_dir)

            # initialize the output data as an empty list
            self.output = []

            # get the output file name
            self.output_file = args.output_file

            # get the boolean flag to indicate whether to output the text translations
            self.output_text_translations = args.output_text_translations

        except Exception as e:
            self.logger.error("Error during configuration: {}".format(e))
            raise e
    
    
    def driver(self):
        try:
            self.logger.info ("PdfScraper::driver")

            # loop through all the files in the input data directory
            for filename in os.listdir(self.input_data_dir):

                # check if the file is a PDF
                if filename.endswith(".pdf"):

                    # open the PDF file using PyMuPDF
                    pdf_file = fitz.open(os.path.join(self.input_data_dir, filename))

                    page = pdf_file[0]

                    text_blocks = page.get_text_blocks()

                    # open the PDF file using PyMuPDF
                    with fitz.open(os.path.join(self.input_data_dir, filename)) as doc:        
                        # Select the first page
                        page = doc[0]

                        # Extract the text from the page with blank lines
                        # NOTE: use getTextBlocks() if you get depricated errors
                        # returns a list of text blocks, each block is a list of 6 items:
                        text_blocks = page.get_text_blocks() 

                        if self.output_text_translations: self.make_text_translations(filename, text_blocks)

                        # Get title of the document
                        title = self.get_title(text_blocks)

                        # Get abstract of the document
                        abstract = self.get_abstract(text_blocks)

                        # Append the title and abstract to the output data
                        self.output.append({"title": title, "abstract": abstract})

            # Save the output data to a JSON file
            with open(self.output_file, 'w') as f:
                json.dump(self.output, f, indent=4)       

        except Exception as e:
            self.logger.error("Error during running the driver: {}".format(e))
    

    """
    Make translations will save the text translations to a file
    It will add a blank line between each text block

    Parameters:
    :param filename: name of the file
    :ptype filename: string
    :param text_blocks: list of text blocks, each block is a list of 6 items:
    :ptype text_blocks: list
    :return: None
    """
    def make_text_translations(self, filename, text_blocks):
        try:
            self.logger.info ("PdfScraper::make_text_translations")

            # Combine the text blocks into a single string with blank lines
            text = ''
            for block in text_blocks:
                text += block[4] + '\n\n'
            
            # Save the text to a file
            with open('text_translations/' + filename + ".txt", 'w', encoding="utf-8") as f:
                f.write(text)

        except Exception as e:
            self.logger.error("Error during making text translations: {}".format(e))
            raise e
    
    
    """
    Get title will return the title of the document
    It is based on the logic that the title will be the first block of text that is not empty
    
    Parameters:
    :param text_blocks: list of text blocks, each block is a list of 6 items:
    :ptype text_blocks: list
    :return: title of the document
    """
    def get_title(self, text_blocks):
        try:
            self.logger.info ("PdfScraper::get_title")

            title = ''
            for block in text_blocks:
                if not title and block[4]:
                    title += block[4]
            
            return title

        except Exception as e:
            self.logger.error("Error during getting the title: {}".format(e))
            raise e
    

    """
    Get abstract will return the abstract of the document
    It is based on the logic that we will first find the block of text that contains the word 'abstract'
    and then the next block of text will be the abstract

    Parameters:
    :param text_blocks: list of text blocks, each block is a list of 6 items:
    :ptype text_blocks: list
    :return: abstract of the document
    """
    def get_abstract(self, text_blocks):
        try:
            self.logger.info ("PdfScraper::get_abstract")

            abstract = ''
            abstract_found = False
            for block in text_blocks:
                if 'abstract' in block[4].lower():
                    abstract_found = True
                    continue
                if abstract_found:
                    abstract += block[4] + ' '
                    break
            
            return abstract

        except Exception as e:
            self.logger.error("Error during getting the abstract: {}".format(e))
            raise e


"""
Parse the command line arguments
"""
def parseCmdLineArgs ():
    # instantiate a ArgumentParser object
    parser = argparse.ArgumentParser (description="PDF Scraper")

    parser.add_argument ("-l", "--loglevel", type=int, default=logging.INFO, choices=[logging.DEBUG,logging.INFO,logging.WARNING,logging.ERROR,logging.CRITICAL], help="logging level, choices 10,20,30,40,50: default 20=logging.INFO")

    parser.add_argument ("-i", "--input_data_dir", default='data', help="Input directory consisting of the PDFs to be scraped, default:input = 'data' ")

    parser.add_argument ("-o", "--output_file", default="output.json", help="Output file to store the extracted data, default:output_file = 'output.json")

    parser.add_argument ("-ott", "--output_text_translations", default=False, help="Boolean flag to indicate whether to output the text translations, default:output_text_translations = False")

    return parser.parse_args()


"""
Main driver program
"""
def main():
    try:
        # obtain a system wide logger and initialize it to debug level to begin with
        logging.info ("Main - acquire a child logger and then log messages in the child")
        logger = logging.getLogger ("PDFScraper")
        
        # first parse the arguments
        logger.debug ("Main: parse command line arguments")
        args = parseCmdLineArgs ()

        # reset the log level to as specified
        logger.debug ("Main: resetting log level to {}".format (args.loglevel))
        logger.setLevel (args.loglevel)
        logger.debug ("Main: effective log level is {}".format (logger.getEffectiveLevel ()))

        # Obtain a publisher application
        logger.debug ("Main: obtain the PDF Scraper object")
        blme = PdfScraper ( logger )

        # configure the object
        logger.debug ("Main: configure the object")
        blme.configure (args)

        # now invoke the driver program
        logger.debug ("Main: invoke driver")
        blme.driver ()
        
    except Exception as e:
        logger.error ("Exception caught in main - {}".format (e))
        return


if __name__ == "__main__":
    # set underlying default logging capabilities
    logging.basicConfig (level=logging.DEBUG,
                       format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
  
    main()