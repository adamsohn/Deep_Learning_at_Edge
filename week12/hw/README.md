# W251 HW12 GPFS FPO & LazyNLP
Adam Sohn
______

### 1. How much disk space is used after step 4? 
> After running the reddit file lists for 96 hours, 3.2M pages were crawled with an additional 4.2M pages with various errors (bad url, connection issue, empty, index, non-ascii, skip). This totals to 7.4M URLs processed, 32% of 23M total set.
### 2. Did you parallelize the crawlers in step 4? If so, how? 
> Yes. 
> Step 1:  The lists (files) of URLs were split between 3 folders in the GPFS file system using `folder_splitter.py` 
> Step 2: On each of 3 nodes, a script was invoked `crawl_x.sh` (where x is node number) which calls `crawl.py` mutiple times in parallel (using `&` operator between calls) for one-third of all assigned lists. All nodes' scripts download text to a folder common between all nodes. 
### 3. Describe the steps to de-duplicate the web pages you crawled.
> To deduplicate web pages, append the function `filter_files` to function `main()` after `create_gutenberg()` in `crawler.py`.  This will require additional functions to be placed in `crawler.py` to handle dependencies of `filter_files`. These additional functions either were already in `crawler.py` or can be found in the [lazynlp git page](https://github.com/chiphuyen/lazynlp/tree/master/lazynlp).

### 4. Submit the list of files you that your LazyNLP spiders crawled (ls -la).
> See [GoogleDrive Link](https://drive.google.com/open?id=1H2B_VgmKdb9vML7mwG67COyw8NU2ciZD)
