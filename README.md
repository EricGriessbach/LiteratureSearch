# Research Paper Citation Visualization with Gephi

This project guides users through the process of visualizing research paper citations as a graph network using Gephi. The instructions cover everything from generating data for custom visualizations from SCOPUS to visualizing pre-existing graphs.

## Getting Started with Pre-existing Graphs

### Installation
1. Download and install Gephi from the [Gephi website](https://gephi.org/).

### Visualizing Graphs
1. Open either `Visualization_Fields.gephi` or `Visualization_Years.gephi`, depending on your focus.
2. Explore and interact with the visualization to gain insights.

## Generating Data for Custom Visualization

### 1. Extract Articles from SCOPUS
- **Script**: Use `import_searchScopus.py` to retrieve articles from SCOPUS, saving the output as `database.csv`.
- **API Key**: Obtain an API key from [SCOPUS](https://dev.elsevier.com/). Set it as an environment variable named `SCOPUS_API_KEY`. Alternatively, you can embed the API key directly in the `import_searchScopus.py` script under the `api_key` variable. Using an environment variable is recommended for security.
- **Search Query**: Adjust the search query in the script. Use `{}` as placeholders for phrases.
- **Note**: SCOPUS limits results to 5,000 articles per query. Divide your search into specific `date_ranges` to bypass this limit.

### 2. Collect Citation and Reference Data
- **Script**: Execute `getCitationReferences.py` to gather citation and reference data for the articles listed in `database.csv`, storing this information in `citations.csv` and `references.csv`, respectively, via Semantic Scholar.

### 3. Prepare Visualization Data
- **Script**: Run `makeCitationMatrix` to generate `edge_attributes.csv` and `node_attributes.csv` for Gephi visualization, and `citation_Matrix.csv` for further analysis (e.g., PCA, t-SNE).

## Visualizing the Graph Network in Gephi

### Setup
1. If not already done, download and install Gephi from the [Gephi website](https://gephi.org/).
2. Import `edge_attributes.csv` and `node_attributes.csv` into the existing workspace in Gephi.

### Interface Overview
- Get acquainted with the three main panels: Overview, Data Laboratory, and Preview, focusing primarily on the Overview panel.

### Configuring the Overview
- **Layout**: Start with the Fruchtermann Reingold algorithm to spread nodes, followed by ForceAtlas 2 until the layout stabilizes.
- **Appearance**: Adjust node sizes based on citation count (2 to 20) and set edge colors to a lighter shade.
- **Community Detection**: Use the Modularity option under Statistics for community detection, facilitating node color coding based on the modularity variable.

### Finalizing in Preview Panel
- Make final aesthetic adjustments, such as reducing edge opacity for better clarity.

## License
Include a license here, if applicable.

## Acknowledgments
Thank any contributors or sources of data here.
