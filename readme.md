# kintextr

## Commands
- `python textualize.py`
- `python textualize.py -a b -id bk/energy`
- `python textualize.py -a r -id bk/energy`
- `python textualize.py -a x -id bk/energy`


## Using Tessearact directly
`tesseract --oem 1 --psm 6 bill_2010_2.jpg stdout`

## Pretty print json
python -m json.tool file.json