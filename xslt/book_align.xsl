<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

    <xsl:variable name="book1" select="document('../xml_files/dost_cap_ende_en.xml')/*" />
    <xsl:variable name="book2" select="document('../xml_files/dost_cap_ende_de.xml')/*" />

	<xsl:template match="/">
		<html>
			<head>
				<title>Bi-Text Aligner</title>
			</head>
            <style>
                table {
                  border-collapse: collapse;
                }
                table, th, td {
                  border: 1px solid black;
                }
                tr:nth-child(odd) {
                  background: #e8eaed
                }
                tr:nth-child(even) {
                  background: #ffffff
                }
                table tr th {
                  font-size: 22px;
                }
                table tr td {
                  font-size: 20px;
                }
            </style>
			<body>
				<h2 align="center">Parallel Corpus</h2>
                <br />
                <xsl:apply-templates select="book/bookInfo" />
                <xsl:apply-templates select="book/content" />
			</body>
		</html>
	</xsl:template>

    <xsl:template match="bookInfo">
        <table border="1" align="center" width="50%" cellpadding="10">
            <tr>
                <td bgcolor="#cccc99" width="8%"><b>Book Name</b></td>
                <td width="21%"><xsl:value-of select="$book1/bookInfo/title" /></td>
                <td width="21%"><xsl:value-of select="$book2/bookInfo/title" /></td>
            </tr>
            <tr>
                <td bgcolor="#cccc99"><b>Book Language</b></td>
                <td><xsl:value-of select="$book1/bookInfo/lang" /></td>
                <td><xsl:value-of select="$book2/bookInfo/lang" /></td>
            </tr>
            <tr>
                <td bgcolor="#cccc99"><b>Is Translation?</b></td>
                <td><xsl:value-of select="$book1/bookInfo/isTranslation" /></td>
                <td><xsl:value-of select="$book2/bookInfo/isTranslation" /></td>
            </tr>
            <tr>
                <td bgcolor="#cccc99"><b>Total Chapters</b></td>
                <td><xsl:value-of select="$book1/bookInfo/totalChapters" /></td>
                <td><xsl:value-of select="$book2/bookInfo/totalChapters" /></td>
            </tr>
            <tr>
                <td bgcolor="#cccc99"><b>Author</b></td>
                <td><xsl:value-of select="$book1/bookInfo/author" /></td>
                <td><xsl:value-of select="$book2/bookInfo/author" /></td>
            </tr>
            <tr>
                <td bgcolor="#cccc99"><b>Source</b></td>
                <td><xsl:value-of select="$book1/bookInfo/source" /></td>
                <td><xsl:value-of select="$book2/bookInfo/source" /></td>
            </tr>
        </table>
        <br />
        <br />
        <br />
    </xsl:template>

    <xsl:template match="content">
        <xsl:for-each select="chapter">
            <xsl:variable name="position" select="position()" />
            <h2 align="center">Chapter - <xsl:value-of select="@num" /></h2>
            <table border="1" align="center" width="80%" cellpadding="10">
                <tr>
                    <th bgcolor="#cccc99" width="40%"><xsl:value-of select="$book1/content/chapter[$position]/@name"/></th>
                    <th bgcolor="#cccc99" width="40%"><xsl:value-of select="$book2/content/chapter[$position]/@name"/></th>
                </tr>
                <xsl:for-each select="sentence">
                    <xsl:variable name="sen_position" select="position()" />
                    <tr>
                        <td><xsl:value-of select="$book1/content/chapter[$position]/sentence[$sen_position]"/></td>
                        <td><xsl:value-of select="$book2/content/chapter[$position]/sentence[$sen_position]"/></td>
                    </tr>
                </xsl:for-each>
            </table>
            <br />
            <br />
        </xsl:for-each>
    </xsl:template>

</xsl:stylesheet>
