CREATE DEFINER=`root`@`localhost` PROCEDURE `BrankoPersonalFindSoftwareProcessProcedure`(
    IN Naziv varchar(50)
)
BEGIN
	DROP TABLE IF EXISTS temp_table;
    CREATE TEMPORARY TABLE temp_table AS
    SELECT 	
        drzava.DR_OZNAKA,
        drzava.DR_NAZIV,
        softverski_proces.ID_PROCESA,
        softverski_proces.PROC_NAZIV,
        poslovni_subjekat.PS_ID,
        poslovni_subjekat.PS_NAZIV
    FROM softverski_proces
    INNER JOIN drzava ON 
        softverski_proces.DR_OZNAKA = drzava.DR_OZNAKA
    INNER JOIN poslovni_subjekat ON 
        softverski_proces.PS_ID = poslovni_subjekat.PS_ID
    WHERE
        (Naziv IS NULL OR softverski_proces.PROC_NAZIV LIKE CONCAT('%', Naziv, '%'));
END