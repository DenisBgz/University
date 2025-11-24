./bin/pyinstaller --onefile \
                                           --hidden-import=game \
                                           --hidden-import=utils \
                                           --hidden-import=decorators \
                                           --hidden-import=file_handler \
                                           --add-data "data/words.txt:data" \
                                           --add-data "data/record.txt:data" \
                                           __main__.py
