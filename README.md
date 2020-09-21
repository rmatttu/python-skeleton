# python-skeleton

Python project template.

## Usage

```bash
python3 example.py source dest
```

## Requirements

* python3
* pip

## Installation

```bash
# edit configure
cp conf/default.yml conf/local.yml
vim conf/local.yml

# virtualenvを使用する時
# python3 -m venv .venv
# source .venv/bin/activate

# install requirements
pip3 install -r requirements.txt

mkdir local
```

here documents.

```bash
cat << EOS > local/input.txt
hello

hoge
fuga
piyo

EOS
```

## License

## Author

