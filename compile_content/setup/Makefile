all:
	echo "- make compile -> Compile the setup.exe file"
	echo "- make clean -> Clean the setup.exe file"
	echo "- make convert -> Convert 'app.zip' to 'app.bytes'"

compile:
	@echo "Compiling the setup.exe file"
	@pyinstaller --noconsole --onefile --add-data "app.bytes;." --icon "logo.ico" install.py
	@echo "Done"

clean:
	@echo "Cleaning the setup.exe file"
	@rm -rf build
	@rm -rf __pycache__
	@rm -rf *.spec
	@echo "Done"

convert:
	@echo "Converting 'app.zip' to 'app.bytes'"
	@python3 convert.py
	@echo "Done"

.phony: clean compile convert all