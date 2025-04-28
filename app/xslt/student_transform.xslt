<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns="http://www.w3.org/1999/xhtml">
  <xsl:output method="text"/>

  <xsl:template match="/student">
    {
      "id": "<xsl:value-of select='id'/>",
      "full_name": "<xsl:value-of select='full_name'/>",
      "birth_date": "<xsl:value-of select='birth_date'/>",
      "faculty": "<xsl:value-of select='faculty'/>",
      "specialty": "<xsl:value-of select='specialty'/>",
      "matricule_id": "<xsl:value-of select='matricule_id'/>",
      "year_of_study": "<xsl:value-of select='year_of_study'/>",
      "college": "<xsl:value-of select='college'/>"
    }
  </xsl:template>
</xsl:stylesheet>
