PREFIX ex: <https://example.org/maintenance/>

DELETE { ?observation ex:legacyAsset ?asset }
INSERT { ?observation ex:forAsset ?asset }
WHERE  { ?observation ex:legacyAsset ?asset }
