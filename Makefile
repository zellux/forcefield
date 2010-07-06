ANTLR_CMD=java -cp antlr-3.1.2.jar org.antlr.Tool

default: ExprParser.py Eval.py

ExprParser.py: Expr.g
	$(ANTLR_CMD) $^

Eval.py: Eval.g
	$(ANTLR_CMD) $^

clean:
	rm -rf *.pyc
	rm -rf ExprParser.py* ExprLexer.py* Expr.tokens
	rm -rf Eval.py* Eval.tokens
