ANTLR_CMD=java -cp antlr-3.1.2.jar org.antlr.Tool

default: CloudScriptParser.py

CloudScriptParser.py: CloudScript.g
	$(ANTLR_CMD) $^

clean:
	rm -rf *.pyc
	rm -rf CloudScriptParser.py CloudScriptLexer.py CloudScript.tokens
