# Game Of Papers - A reccomendation system for research papers.

## Use the model using the transformer library
Easiest way to get started with the model is using it with the transformers library

```
from transformers import AutoTokenizer, AutoModel

tokenizer = AutoTokenizer.from_pretrained("allenai/scibert_scivocab_uncased")

model = AutoModel.from_pretrained("adit-negi/recommendor-bert")
```

**Demo**
https://master--rococo-froyo-3cec9b.netlify.app/home

## Training the model

![Overview](./bert-based-triplet/asset/finetune.png)

### Installation
    pip install -r requirement.txt

### Usage

**Train**
```
python train_single.py --epochs 50 --batch_size 128 --clip 1.0 --lr 1e-3 --embed_dim 300 \
 --freeze False --space_joiner True --dropout 0.2 \
 --loss_fn triplet --max_len 30 \
 --PRE_TRAINED_MODEL_NAME 'bert-base-uncased' \
 --model_path './ckpt/best_model_v6_triplet' \
 --train_dir './data/14k_data.csv' \
 --use_aux True --use_aug_data True
```

**TrainScibert**
```
python3 train_single.py --epochs 50 --batch_size 128 --clip 1.0 --lr 1e-3 --embed_dim 300 \
 --freeze False --space_joiner True --dropout 0.2 \
 --loss_fn triplet --max_len 30 \
 --PRE_TRAINED_MODEL_NAME 'allenai/scibert_scivocab_uncased' \
 --model_path './ckpt/scibert_model_v6_triplet_2' \
 --train_dir './data/paper_triplet_data.csv' \
 --use_aux True --use_aug_data True
```

**TestDB**
```
python evaluate_single.py --embed_dim 300 \
 --freeze False --space_joiner True --dropout 0.2 \
 --loss_fn triplet --max_len 30 \
 --PRE_TRAINED_MODEL_NAME 'emilyalsentzer/Bio_ClinicalBERT' \
 --model_path './ckpt/best_model_v6_triplet' \
 --train_dir './data/100k_data.csv'
```



**Inference**
```
python inference.py --embed_dim 300 \
 --PRE_TRAINED_MODEL_NAME 'emilyalsentzer/Bio_ClinicalBERT' \
 --model_path './ckpt/best_model_v6_triplet' \
```


## Testing the model against baselines
Easy way to test is to run ```python3 baseline_model_experiments/calculate_metrics.py```
This already runs a bunch of baseline models for you and gives you the result.

### Compare our model against any pretrained model on huggingface

1. Run any baseline model by navigating to baseline_model_experiments/test_any_huggingface_model/huggingface_pretrained.py 

    1.1 Add the name of the model you want to test in AutoModel function 
2. Run the file, it will create a sample.json, with embeddings and sorted reccomendations for papers. 
3. Read the sample.json, append it to the baseline_results list in calculate_metrics.py file and run it. 

# Running the webserver
## Dockerizing Flask with Postgres, Gunicorn, and Nginx and run this locally or in production

## Want to learn how to build this?

Check out the [post](https://testdriven.io/blog/dockerizing-flask-with-postgres-gunicorn-and-nginx).

## Want to use this project?

### Development

Uses the default Flask development server.

1. Rename *.env.dev-sample* to *.env.dev*.
1. Update the environment variables in the *docker-compose.yml* and *.env.dev* files.
    - (M1 chip only) Remove `-slim-buster` from the Python dependency in `services/web/Dockerfile` to suppress an issue with installing psycopg2
1. Build the images and run the containers:

    ```sh
    $ docker-compose up -d --build
    ```

    Test it out at [http://localhost:5000](http://localhost:5000). The "web" folder is mounted into the container and your code changes apply automatically.
1. To seed data into the database download the sql dump from - [http://drive.google.com/sqldata](https://drive.google.com/file/d/12RQX0gLJ2N4SzQ1BqACmjTyM-dwkk555/view?usp=share_link) and run `pg_dump -U hello_flask -h 127.0.0.1 hello_flask_dev > gameofpapers.sql`. When prompted enter the password provided in the docker-compose file.

### Production

Uses gunicorn + nginx.

1. Rename *.env.prod-sample* to *.env.prod* and *.env.prod.db-sample* to *.env.prod.db*. Update the environment variables.
1. Build the images and run the containers:

    ```sh
    $ docker-compose -f docker-compose.prod.yml up -d --build
    ```

    Test it out at [http://localhost:1337](http://localhost:1337). No mounted folders. To apply changes, the image must be re-built.
