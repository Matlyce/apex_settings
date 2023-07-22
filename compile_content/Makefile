all:
	echo "- make compile -> Compile the app.exe file"
	echo "- make clean -> Clean the app.exe file"

compile:
	@echo "Compiling the app.exe file"
	@pyinstaller --noconsole --onefile --name ApexSettings --icon logo.ico --add-data "./Apex-Black.ttf;." --add-data "./logo.ico;."  main.py
	@echo "Done"

clean:
	@echo "Cleaning the app.exe file"
	@rm -rf build
	@rm -rf __pycache__
	@rm -rf *.spec
	@echo "Done"

.phony: clean compile all
