## Installation
Install python using conda: [install Anaconda](https://docs.conda.io/projects/conda/en/stable/user-guide/install/index.html)
create Env:
```bash
conda create --name myenv
```
activate Env:
```bash
conda activate myenv
```
install packages:
```bash
pip install -r requirements.txt
```

## Executing
Run Api project:
```bash
flask --app app run --debug
```

## Documentation
[Swagger endpoints](http://localhost:5000/swagger-ui/)

## Testing
install nodejs (more details in app README) and install postman-cli:
```bash
npm install -g postman-cli
```
To initialize the Database
```bash
postman request POST 'http://127.0.0.1:5000/init' \ --body ''
```

## Train Experiments
access jupyter notebook `batch-train.ijpynb`
download your AzureML config.json and place in project root
set dataset name and run notebook