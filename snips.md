# vidi snips
snips are useful code snippets, command line examples, etc

#### Batch convert images
```Shell
mogrify -path ./small -filter Lanczos -sampling-factor 1x1 -resize 1000 -unsharp 1.5x1+0.5+0.02 -quality 90 ./full/*.jpg
```

#### To ping the server
```Shell
./cli.py -c ping
```

#### To load an index from disk
```Shell
./cli.py -c load -i load.dat
```

#### To save the current index
```Shell
./cli.py -c save -i save.dat
```

#### To clear the current index
```Shell
./cli.py -c clear
```

#### To add an image to the index
*FILE is a path to a JPEG*
```Shell
./cli.py -c add -i FILE -d ID
```

#### To add all images within a directory to the index
```Shell
./cli.py -c bulk -i DIRECTORY -d START
```

### To search for matches in the current index
```Shell
./cli.py -c search -i FILE
```