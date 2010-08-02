/**
 * ForceField syntax forSyntaxHighlighter
 * http://alexgorbatchev.com/SyntaxHighlighter
 *
 * SyntaxHighlighter is donationware. If you are using it, please donate.
 * http://alexgorbatchev.com/SyntaxHighlighter/donate.html
 *
 */
;(function()
  {
    // CommonJS
    typeof(require) != 'undefined' ? SyntaxHighlighter = require('shCore').SyntaxHighlighter : null;

    function Brush()
    {
      var keywords =	'IF FUNC ASSERT RETURN DO WHILE HTTP WRITE_LOG SERVER_TIME ' +
	'SET ELSE END REMOTE';

      this.regexList = [
	{ regex: SyntaxHighlighter.regexLib.doubleQuotedString,	css: 'string' },			// strings
	{ regex: /^\s*#.*$/gm, css: 'preprocessor' },          // preprocessor tags like #region and #endregion
	{ regex: new RegExp(this.getKeywords(keywords), 'gm'), css: 'keyword' }	// vb keyword
      ];

      this.forHtmlScript(SyntaxHighlighter.regexLib.aspScriptTags);
    };

    Brush.prototype = new SyntaxHighlighter.Highlighter();
    Brush.aliases = ['ff'];

    SyntaxHighlighter.brushes.Ff = Brush;

    // CommonJS
    typeof(exports) != 'undefined' ? exports.Brush = Brush : null;
})();
