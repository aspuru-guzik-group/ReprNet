# remember to first install twine by python3 -m pip install --upgrade build
cd ..
python3 -m build
python3 -m twine upload dist/*
rm -r dist