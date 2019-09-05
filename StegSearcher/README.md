# Steghide Searcher

Steghide Searcher is a simple python script to find hidden data in Last Significant Bits(LSB) of images.

Steghide comes from [Steghenography](https://searchsecurity.techtarget.com/definition/steganography).

## Usage

This script works on only Python3 version.

```sh
python3 SteghideSearcher.py ["Image Path"] ["Key Word"] ["Iteration"]

["Image Path"] : Image that will be search.
["Key Word"]   : Word that will be find.
["Iteraion"]   : Binary shifting value.

Example Usage:
python3 SteghideSearcher.py ./example.jpg word 16

```

Warning!
Make sure your python version. Sometimes Python 3 can be run only "python" command on your shell. 

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
