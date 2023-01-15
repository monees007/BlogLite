SCRIPTPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
export PYTHONPATH="${PYTHONPATH}:$SCRIPTPATH"
if [ -d "venv" ];
then
    echo "venv folder exists. Installing using pip"
else
    echo "creating venv and install using pip"
    python3 -m venv venv
fi

# Activate virtual env
. venv/bin/activate

# Upgrade the PIP
pip install --upgrade pip
$ Install the requirements

pip install -r requirements.txt

export ENV=production
python -m flask run