CREATE DEFINER=`root`@`localhost` PROCEDURE `BrankoPersonalFetchSoftwareProcessProcedure`(
    IN Drzava varchar(50),
	IN Kompanija int,
    IN Proces int,
    IN Naziv varchar(50)
)
BEGIN
	DROP TABLE IF EXISTS temp_table;
    CREATE TEMPORARY TABLE temp_table AS
    SELECT 	
		sp.*,
        struktura_procesa.AKT_OZNAKA,
        struktura_procesa.AKT_VERZIJA,
        struktura_aktivnosti.AKT_DATFORM,
        katalog_aktivnosti.AKT_NAZIV
	FROM softverski_proces sp 
	INNER JOIN poslovni_subjekat ON 
        sp.PS_ID = poslovni_subjekat.PS_ID
	INNER JOIN struktura_procesa ON 
		sp.ID_PROCESA = struktura_procesa.ID_PROCESA AND 
        sp.PS_ID = struktura_procesa.PS_ID AND 
        sp.DR_OZNAKA = struktura_procesa.DR_OZNAKA
	INNER JOIN struktura_aktivnosti ON 
		struktura_procesa.AKT_OZNAKA = struktura_aktivnosti.AKT_OZNAKA AND
        struktura_procesa.AKT_VERZIJA = struktura_aktivnosti.AKT_VERZIJA
	INNER JOIN katalog_aktivnosti ON 
		struktura_aktivnosti.AKT_OZNAKA = katalog_aktivnosti.AKT_OZNAKA
	
    WHERE 
		sp.PROC_NAZIV = Naziv and 
		sp.ID_PROCESA = Proces and
		sp.PS_ID = Kompanija and
		sp.DR_OZNAKA = Drzava;
END