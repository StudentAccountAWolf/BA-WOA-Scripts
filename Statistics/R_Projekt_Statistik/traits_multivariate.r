#!/usr/bin/env Rscript




# ---------- Preparations ----------
# Load libraries
library(parallel)               # Detect number of cpu cores
library(foreach)                # For multicore parallel
#library(doMC)                   # For multicore parallel
library(RColorBrewer)           # For colors
#library(MSnbase)                # MS features
#library(xcms)                   # Swiss army knife for metabolomics
#library(CAMERA)                 # Metabolite Profile Annotation
#library(Spectra)                # Spectra package needed for XCMS3
library(vegan)
library(multcomp)               # For Tukey test
library(Hmisc)                  # For correlation test
library(ggplot2)
library(gplots)                 # For fancy heatmaps
#library(circlize)               # For sunburst plot
#library(plotrix)                # For sunburst plot
library(caret)                  # Swiss-army knife for statistics
library(pls)                    # PLS
#library(spls)                   # sparse PLS
library(randomForest)           # Random Forest
library(pROC)                   # Evaluation metrics
library(PRROC)                  # Evaluation metrics
library(multiROC)               # Evaluation metrics
#library(chemodiv)               # Chemodiversity (Petren 2022)
#library(rcdk)                   # CDK
#library(Rcpi)                   # Molecular descriptors
#library(rinchi)                 # Converting SMILES to InchiKey
library(plotly)                 # For creating html plots
library(htmlwidgets)            # For creating html plots
library(shiny)                  # HTML in R
#library(sunburstR)              # HTML-sunburst plots
library(heatmaply)              # HTML heatmaps
library(phytools)               # For phylogeny analyses
library(ape)                    # For phylogeny analyses
library(treeio)                 # For phylogeny analyses
library(phangorn)               # For phylogeny analyses
library(cba)                    # For phylogeny analyses
library(pvclust)                # For phylogeny clustering
library(ggplot2)                # For plotting
library(ggtree)                 # For plotting
library(ggfortify)              # For plotting
#library(rentrez)                # For searching Genbank
library(rpart)                  # For decision/regression trees
library(rpart.plot)             # For decision/regression trees
library(rattle)                 # For decision/regression trees
library(party)                  # For conditional decision trees


#-------------------------------------------------------------------------------

# Laden Sie das 'renv' Paket
library(renv)

# Funktion, um Abhängigkeiten zu ermitteln
get_dependencies <- function(project_path) {
  # Setzen Sie den Pfad zum Projektverzeichnis
  setwd(project_path)
  
  # Ermitteln Sie die Abhängigkeiten
  dependencies <- renv::dependencies()
  
  # Erstellen Sie ein Dataframe mit den Paketnamen und den Dateien, in denen sie gefunden wurden
  dep_df <- data.frame(Package = dependencies$Package, File = dependencies$Source)
  
  # Rückgabe des Dataframes
  return(dep_df)
}

# Verwendung der Funktion
# Ersetzen Sie 'path/to/your/project' mit dem tatsächlichen Pfad zu Ihrem Projekt
project_path <- 'M:/Programmieren/Arbeitsordner/Learning/Statistics'
dep_df <- get_dependencies(project_path)

# Ausgabe der ermittelten Pakete
print(dep_df)

#-------------------------------------------------------------------------------



#-------------------------------------------------------------------------------
print_package_versions <- function() {
  # List of packages
  packages <- c(
    "ape", "caret", "cba", "foreach", "ggfortify", "ggplot2", "ggtree", "gplots", 
    "heatmaply", "Hmisc", "htmlwidgets", "multcomp", "multiROC", "parallel", 
    "party", "phangorn", "phytools", "plotly", "pls", "pROC", "PRROC", "pvclust", 
    "randomForest", "rattle", "RColorBrewer", "rotl", "rpart", "rpart.plot", 
    "shiny", "treeio", "vegan", "adabag", "base", "bnclassify", "Boruta", 
    "circlize", "doParallel", "dummies", "e1071", "httr", "lmerTest", "mixOmics", 
    "mlr", "mltest", "multcomp", "naivebayes", "ontologyIndex", "plotrix", 
    "ropls", "scales"
  )
  
  # Initialize empty vector to store results
  versions <- character(length(packages))
  
  # Loop through packages and get version
  for (i in seq_along(packages)) {
    if (requireNamespace(packages[i], quietly = TRUE)) {
      vers <- packageVersion(packages[i])
      if (is.list(vers)) {
        # If multiple versions are installed, take the first one
        versions[i] <- paste0('"', packages[i], " ", vers[[1]], '"')
      } else {
        versions[i] <- paste0('"', packages[i], " ", vers, '"')
      }
    } else {
      versions[i] <- NA
    }
  }
  
  # Print results
  for (j in seq_along(packages)) {
    cat(versions[j], "\n")
  }
}


print_package_versions()



#-------------------------------------------------------------------------------





# Setup R error handling to go to stderr
#options(show.error.messages=F, error=function() { cat(geterrmessage(), file=stderr()); q("no",1,F) } )

# Set locales and encoding
#loc <- Sys.setlocale("LC_MESSAGES", "en_US.UTF-8")
#loc <- Sys.setlocale(category="LC_ALL", locale="C")
#options(encoding="UTF-8")

# Set options
options(stringAsfactors=FALSE, useFancyQuotes=FALSE)

# Multicore parallel
#nSlaves <- detectCores(all.tests=FALSE, logical=FALSE)
#nSlaves <- 12
#registerDoMC(nSlaves)



# ---------- User variables ----------
# Working directory
setwd("M:/Programmieren/Arbeitsordner/Learning/Statistics/")

# Data directory
mzml_dir <- "M:/Programmieren/Arbeitsordner/Learning/Statistics/"

# Preparations for plotting
par(mfrow=c(1,1), mar=c(4,4,4,1), oma=c(0,0,0,0), cex.axis=0.9, cex=0.8)

# Save and load RData
#save.image()
load(".RData")

# Load iESTIMATE functions
source("_functions.r")

# Set up parallel processing
#library(e1071)
#library(doMC)
#registerDoMC(nSlaves)



# ---------- Preparations ----------

measurements <- read.delim(file.choose(), header=T, stringsAsFactors =T)
measurements_temp <- measurements
measurements_temp[is.na(measurements_temp)] <- 0
measurements_temp$MEX[measurements_temp$MEX == TRUE] <- 1
measurements_temp$MEX[measurements_temp$MEX == FALSE] <- 0
measurements_temp$CS <- as.numeric(as.factor(measurements_temp$CS)) # 4=square; 3=prosenchymatic; 2=hexagonal
measurements_temp$GF <- as.numeric(as.factor(measurements_temp$GF)) # 1=apocarp; 2=pleurocarp
measurements_temp$Plant <- as.numeric(as.factor(measurements_temp$Plant))
#measurements_temp$LLSH[which(is.na(measurements_temp$LLSH))] <- 0
#measurements_temp$SHL[which(is.na(measurements_temp$SHL))] <- 0
#measurements_temp$ML[which(is.na(measurements_temp$ML))] <- 0
#measurements_temp$MW[which(is.na(measurements_temp$MW))] <- 0
#measurements_temp$MH[which(is.na(measurements_temp$MH))] <- 0
#measurements_temp$MA[which(is.na(measurements_temp$MA))] <- 0
#measurements_temp$MTC[which(is.na(measurements_temp$MTC))] <- 0
#measurements_temp$MV[which(is.na(measurements_temp$MV))] <- 0
#measurements_temp$LVTMV[which(is.na(measurements_temp$LVTMV))] <- 0
#measurements_temp$LVTMVP[which(is.na(measurements_temp$LVTMVP))] <- 0



leaf_traits <- subset(measurements_temp, measurements_temp$Measurement == "microscopy")
leaf_traits <- leaf_traits[ ,0:36]
rownames(leaf_traits) <- leaf_traits$Rownames

mass_traits <- subset(measurements_temp, measurements_temp$Measurement == "weight")
mass_traits <- mass_traits[ ,c(1:9, 37:49)]
rownames(mass_traits) <- mass_traits$Rownames

cell_traits <- subset(measurements_temp, measurements_temp$Measurement == "cell")
cell_traits <- cell_traits[ ,c(1:9, 50:51)]
cell_traits <- cell_traits[!grepl("Average$", cell_traits$WOA_measurement_Species_Plant_Leaf), ] # Average Werte löschen
rownames(cell_traits) <- cell_traits$Rownames


measurements_temp_2 <- measurements_temp[, 0:49]
measurements_temp_2 <- subset(measurements_temp_2, measurements_temp_2$Measurement != "cell")
rownames(measurements_temp_2) <- measurements_temp_2$Rownames


#leaf_traits <- measurements[1:71, 8:47]
#leaf_traits <- measurements[1:71, 8:34]
#rownames(leaf_traits) <- measurements$WOA_measurement_Species_Plant_Leaf[1:71]
#leaf_traits$MEX[leaf_traits$MEX == TRUE] <- 1
#leaf_traits$MEX[leaf_traits$MEX == FALSE] <- 0
#leaf_traits$CS <- as.numeric(as.factor(leaf_traits$CS))
#leaf_traits$LLSH[which(is.na(leaf_traits$LLSH))] <- 0
#leaf_traits$SHL[which(is.na(leaf_traits$SHL))] <- 0
#leaf_traits$ML[which(is.na(leaf_traits$ML))] <- 0
#leaf_traits$MW[which(is.na(leaf_traits$MW))] <- 0
#leaf_traits$MH[which(is.na(leaf_traits$MH))] <- 0
#leaf_traits$MA[which(is.na(leaf_traits$MA))] <- 0
#leaf_traits$MTC[which(is.na(leaf_traits$MTC))] <- 0
#leaf_traits$MV[which(is.na(leaf_traits$MV))] <- 0
#leaf_traits$LVTMV[which(is.na(leaf_traits$LVTMV))] <- 0
#leaf_traits$LVTMVP[which(is.na(leaf_traits$LVTMVP))] <- 0

#leaf_traits[is.na(leaf_traits)] <- 0

# Species factor LEAF
species <- unique(leaf_traits$Species_short)
species_samples_leaf <- as.factor(leaf_traits$Species_short)

# Species factor MASS
species_mass <- unique(mass_traits$Species_short)
species_samples_mass <- as.factor(mass_traits$Species_short)

# Species factor CELL
species_cell <- unique(cell_traits$Species_short)
species_samples_cell <- as.factor(cell_traits$Species_short)

species_temp <- unique(measurements_temp_2$Species_short)
species_samples_temp <- as.factor(measurements_temp_2$Species_short)

# Color vector
species_colors <- c("darkblue", "dodgerblue2", "deepskyblue4", "hotpink3", "mediumpurple3", "plum3", "peachpuff3", "palegreen4", "goldenrod3")
species_colors_samples_leaf <- sapply(species_samples_leaf, function(x) { x <- species_colors[which(x==unique(species_samples_leaf))] } )
species_colors_samples_mass <- sapply(species_samples_mass, function(x) { x <- species_colors[which(x==unique(species_samples_mass))] } )
species_colors_samples_cell <- sapply(species_samples_cell, function(x) { x <- species_colors[which(x==unique(species_samples_cell))] } )
species_colors_temp <- sapply(species_samples_temp, function(x) { x <- species_colors[which(x==unique(species_samples_temp))] } )

# ---------- Variation partitioning ----------
# Study factors
# leaf_traits[, 7:ncol(leaf_traits)]
model_varpart_leaf <- varpart(scale(leaf_traits[,8:ncol(leaf_traits)], scale=TRUE, center=TRUE), ~ species_samples_leaf, ~ leaf_traits$GF, ~ leaf_traits$MEX, ~ leaf_traits$Plant)
plot(model_varpart_leaf, Xnames=c("species","carpie","midrib","plant"), cutoff=0, cex=1.2, id.size=1.2, digits=1, bg=c("blue","green","yellow","red"))









# ---------- PCA LEAF ---------
model_pca_leaf <- prcomp(leaf_traits[,8:ncol(leaf_traits)], scale=TRUE, center=TRUE)

# classic plot
plot(model_pca_leaf$x[, 1], model_pca_leaf$x[, 2], pch=19, main="PCA",
	 xlab=paste0("PC1: ", format(summary(model_pca_leaf)$importance[2, 1] * 100, digits=3), " % variance"),
	 ylab=paste0("PC2: ", format(summary(model_pca_leaf)$importance[2, 2] * 100, digits=3), " % variance"),
	 col=species_colors_samples_leaf, cex=2)
#grid()
#text(model_pca_leaf$x[, 1], model_pca_leaf$x[, 2], labels=rownames(leaf_traits), col=species_colors_samples_leaf, pos=3, cex=0.8)
legend("topleft", bty="n", legend=species, pch=19, col=species_colors, pt.cex=1.3, cex=1, y.intersp=0.7, text.width=0.1)

# explained variance
screeplot(model_pca_leaf, bstick=TRUE, type=c("barplot", "lines"), npcs=min(20, length(model_pca_leaf$sdev)), ptype="o", bst.col="red", bst.lty="solid", xlab="Component", ylab="Inertia", main="Broken stick test of PCA", legend=TRUE)

# ---------- PCA MASS ----------
model_pca_mass <- prcomp(mass_traits[,8:ncol(mass_traits)], scale=TRUE, center=TRUE)

# classic plot
plot(model_pca_mass$x[, 1], model_pca_mass$x[, 2], pch=19, main="PCA",
     xlab=paste0("PC1: ", format(summary(model_pca_mass)$importance[2, 1] * 100, digits=3), " % variance"),
     ylab=paste0("PC2: ", format(summary(model_pca_mass)$importance[2, 2] * 100, digits=3), " % variance"),
     col=species_colors_samples_mass, cex=2)
grid()
#text(model_pca_mass$x[, 1], model_pca_mass$x[, 2], labels=rownames(leaf_traits), col=species_colors_samples_mass, pos=3, cex=0.5)
legend("bottomleft", bty="n", legend=species, pch=19, col=species_colors, pt.cex=0.8, cex=0.9, y.intersp=0.8, text.width=0.1)

# explained variance
screeplot(model_pca_mass, bstick=TRUE, type=c("barplot", "lines"), npcs=min(20, length(model_pca_mass$sdev)), ptype="o", bst.col="red", bst.lty="solid", xlab="Component", ylab="Inertia", main="Broken stick test of PCA", legend=TRUE)


#---------- PCA CELL ------------
model_pca_cell <- prcomp(cell_traits[,8:ncol(cell_traits)], scale=TRUE, center=TRUE)

# classic plot
plot(model_pca_cell$x[, 1], model_pca_cell$x[, 2], pch=19, main="PCA",
     xlab=paste0("PC1: ", format(summary(model_pca_cell)$importance[2, 1] * 100, digits=3), " % variance"),
     ylab=paste0("PC2: ", format(summary(model_pca_cell)$importance[2, 2] * 100, digits=3), " % variance"),
     col=species_colors_samples_cell, cex=2)
grid()
text(model_pca_cell$x[, 1], model_pca_cell$x[, 2], labels=rownames(leaf_traits), col=species_colors_samples_cell, pos=3, cex=0.5)
legend("bottom", bty="n", legend=species, pch=19, col=species_colors, pt.cex=0.8, cex=0.8, text.width=0.1, adj=1.3)

# explained variance
screeplot(model_pca_cell, bstick=TRUE, type=c("barplot", "lines"), npcs=min(20, length(model_pca_cell$sdev)), ptype="o", bst.col="red", bst.lty="solid", xlab="Component", ylab="Inertia", main="Broken stick test of PCA", legend=TRUE)







#LEAF
# ---------- Regression / Decision Tree ----------
model_rpart_leaf <- f.select_features_rpart_caret(feat_matrix=leaf_traits[,8:ncol(leaf_traits)], sel_factor=species_samples_leaf, sel_colors=species_colors_samples_leaf, tune_length=8, quantile_threshold=0.95, plot_roc_filename=NULL)
print(model_rpart_leaf$`_multiclass_metrics_`)
print(model_rpart_leaf$`_model_r2_`)
# Plot
rpart.plot(prune(model_rpart_leaf$`_finalModel_`, cp=0.05), box.palette=0, type=5, extra=02, under=TRUE, tweak=1.35, leaf.round=0)
# Print selected variables
model_rpart_leaf$`_finalModel_`


#MASS
model_rpart_mass <- f.select_features_rpart_caret(feat_matrix=mass_traits[,8:ncol(mass_traits)], sel_factor=species_samples_mass, sel_colors=species_colors_samples_mass, tune_length=8, quantile_threshold=0.95, plot_roc_filename=NULL)
print(model_rpart_mass$`_multiclass_metrics_`)
print(model_rpart_mass$`_model_r2_`)
# Plot
rpart.plot(prune(model_rpart_mass$`_finalModel_`, cp=0.05), box.palette=0, type=5, extra=02, under=TRUE, tweak=1.35, leaf.round=0)
# Print selected variables
model_rpart_mass$`_finalModel_`

#CELL
model_rpart_cell <- f.select_features_rpart_caret(feat_matrix=cell_traits[,8:ncol(cell_traits)], sel_factor=species_samples_cell, sel_colors=species_colors_samples_cell, tune_length=8, quantile_threshold=0.95, plot_roc_filename=NULL)
print(model_rpart_cell$`_multiclass_metrics_`)
print(model_rpart_cell$`_model_r2_`)
# Plot
rpart.plot(prune(model_rpart_cell$`_finalModel_`, cp=0.05), box.palette=0, type=5, extra=02, under=TRUE, tweak=1.35, leaf.round=0)
# Print selected variables
model_rpart_cell$`_finalModel_`


#All
model_rpart_temp <- f.select_features_rpart_caret(feat_matrix=measurements_temp_2[,8:ncol(measurements_temp_2)], sel_factor=species_samples_temp, sel_colors=species_colors_temp, tune_length=8, quantile_threshold=0.95, plot_roc_filename=NULL)
print(model_rpart_leaf$`_multiclass_metrics_`)
print(model_rpart_leaf$`_model_r2_`)
# Plot
rpart.plot(prune(model_rpart_temp$`_finalModel_`, cp=0.05), main = "Entscheidungsbaum der Blatt- und Gewichtseigenschaften", box.palette=0, type=5, extra=02, under=TRUE, tweak=1.15, leaf.round=1, fallen.leaves=FALSE, split.cex=0.9, branch.lwd = 1.8)
# Print selected variables
model_rpart_leaf$`_finalModel_`




#LEAF
# ---------- Variable selection with Random Forest ----------
model_rf_leaf <- f.select_features_random_forest(feat_matrix=leaf_traits[,8:ncol(leaf_traits)], sel_factor=species_samples_leaf, sel_colors=species_colors_samples_leaf, tune_length=10, quantile_threshold=0.999, plot_roc_filename=NULL)
print(paste("Number of selected variables:", f.count.selected_features(sel_feat=model_rf_leaf$`_selected_variables_`)))
f.heatmap.selected_features(feat_list=leaf_traits, sel_feat=model_rf_leaf$`_selected_variables_`, sample_colors=species_colors_samples_leaf, plot_width=4, plot_height=5, cex_col=0.5, cex_row=0.3, filename=NULL, main="Random Forest")
model_rf_leaf$`_selected_variables_`
model_rf_leaf$`_multiclass_metrics_`
model_rf_leaf$`_model_r2_`

#MASS
model_rf_mass <- f.select_features_random_forest(feat_matrix=mass_traits[,8:ncol(mass_traits)], sel_factor=species_samples_mass, sel_colors=species_colors_samples_mass, tune_length=10, quantile_threshold=0.999, plot_roc_filename=NULL)
print(paste("Number of selected variables:", f.count.selected_features(sel_feat=model_rf_mass$`_selected_variables_`)))
f.heatmap.selected_features(feat_list=mass_traits, sel_feat=model_rf_mass$`_selected_variables_`, sample_colors=species_colors_samples_mass, plot_width=4, plot_height=5, cex_col=0.5, cex_row=0.3, filename=NULL, main="Random Forest")
model_rf_mass$`_selected_variables_`
model_rf_mass$`_multiclass_metrics_`
model_rf_mass$`_model_r2_`

#CELL
model_rf_cell <- f.select_features_random_forest(feat_matrix=cell_traits[,8:ncol(cell_traits)], sel_factor=species_samples_cell, sel_colors=species_colors_samples_cell, tune_length=10, quantile_threshold=0.999, plot_roc_filename=NULL)
print(paste("Number of selected variables:", f.count.selected_features(sel_feat=model_rf_cell$`_selected_variables_`)))
f.heatmap.selected_features(feat_list=cell_traits, sel_feat=model_rf_cell$`_selected_variables_`, sample_colors=species_colors_samples_cell, plot_width=4, plot_height=5, cex_col=0.5, cex_row=0.3, filename=NULL, main="Random Forest")
model_rf_cell$`_selected_variables_`
model_rf_cell$`_multiclass_metrics_`
model_rf_cell$`_model_r2_`





#LEAF
# ---------- PCA with loadings ----------
model_pca_leaf <- prcomp(leaf_traits[, c(model_rf_leaf$`_selected_variables_`)], scale=TRUE, center=TRUE)
#model_pca <- prcomp(leaf_traits[, c("LLSH", "MTC", "LDMC", "DSLM", "VPL")], scale=TRUE, center=TRUE)

# ggplot
autoplot(model_pca_leaf, data=leaf_traits, size=3, color=species_colors_samples_leaf,
         loadings=TRUE, loadings.color="black",
         loadings.label=TRUE, loadings.label.hjust=-1, loadings.label.vjust=1, loadings.label.repel=TRUE, loadings.label.size=4.2, loadings.label.color="black",loadings.arrow.size=5 ) +
  theme(panel.grid.minor=element_line(color="lightgrey", size=0.25, linetype=3),
        panel.grid.major=element_line(color="grey", size=0.5, linetype=3),
        panel.background=element_blank(),
        panel.border=element_rect(color="black", fill=NA, size=1) ) +
  scale_color_manual(values=as.character(species_colors_samples_leaf), labels=gsub(x=species_colors, pattern="\\.", replacement="\\. ")) +
  scale_fill_manual(values=as.character(species_colors_samples_leaf)) +
  guides(shape=guide_legend(override.aes=list(size=1))) +
  theme(legend.position='bottom', legend.direction='vertical', plot.title=element_text(hjust=0.5), axis.title = element_text(size = 13), axis.text = element_text(size = 12)) +
  labs(title="PCA der signifikantesten Blatteigenschaften", title.fontface="bold", x=paste0("PC1: ", format(summary(model_pca_leaf)$importance[2, 1] * 100, digits=3), " % variance"), y=paste0("PC2: ", format(summary(model_pca_leaf)$importance[2, 2] * 100, digits=3), " % variance"))



#MASS
model_pca_mass <- prcomp(mass_traits[, c(model_rf_mass$`_selected_variables_`)], scale=TRUE, center=TRUE)
#model_pca <- prcomp(leaf_traits[, c("LLSH", "MTC", "LDMC", "DSLM", "VPL")], scale=TRUE, center=TRUE)

# ggplot
autoplot(model_pca_mass, data=mass_traits, size=4, color=species_colors_samples_mass,
         loadings=TRUE, loadings.color="black",
         loadings.label=TRUE, loadings.label.hjust=0, loadings.label.vjust=0, loadings.label.repel=TRUE, loadings.label.size=3, loadings.label.color="black" ) +
  theme(panel.grid.minor=element_line(color="lightgrey", size=0.25, linetype=3),
        panel.grid.major=element_line(color="grey", size=0.5, linetype=3),
        panel.background=element_blank(),
        panel.border=element_rect(color="black", fill=NA, size=1) ) +
  scale_color_manual(values=as.character(species_colors_samples_mass), labels=gsub(x=species_colors_samples_mass, pattern="\\.", replacement="\\. ")) +
  scale_fill_manual(values=as.character(species_colors_samples_mass)) +
  guides(shape=guide_legend(override.aes=list(size=2))) +
  theme(legend.position='bottom', legend.direction='vertical', plot.title=element_text(hjust=0.5)) +
  labs(title="PCA der signifikantesten Gewichtseigenschaften", title.fontface="bold", x=paste0("PC1: ", format(summary(model_pca_mass)$importance[2, 1] * 100, digits=3), " % variance"), y=paste0("PC2: ", format(summary(model_pca_mass)$importance[2, 2] * 100, digits=3), " % variance"))


autoplot(model_pca_mass, data=mass_traits, size=3, color=species_colors_samples_mass,
         loadings=TRUE, loadings.color="black",
         loadings.label=TRUE, loadings.label.hjust=1, loadings.label.vjust=1, loadings.label.repel=TRUE, loadings.label.size=4, loadings.label.color="black",loadings.arrow.size=5 ) +
  theme(panel.grid.minor=element_line(color="lightgrey", size=0.25, linetype=3),
        panel.grid.major=element_line(color="grey", size=0.5, linetype=3),
        panel.background=element_blank(),
        panel.border=element_rect(color="black", fill=NA, size=1) ) +
  scale_color_manual(values=as.character(species_colors_samples_mass), labels=gsub(x=species_colors_samples_mass, pattern="\\.", replacement="\\. ")) +
  scale_fill_manual(values=as.character(species_colors_samples_mass)) +
  guides(shape=guide_legend(override.aes=list(size=1))) +
  theme(legend.position='bottom', legend.direction='vertical', plot.title=element_text(hjust=0.5), axis.title = element_text(size = 13), axis.text = element_text(size = 12)) +
  labs(title="PCA der signifikantesten Gewichtseigenschaften", title.fontface="bold", x=paste0("PC1: ", format(summary(model_pca_mass)$importance[2, 1] * 100, digits=3), " % variance"), y=paste0("PC2: ", format(summary(model_pca_mass)$importance[2, 2] * 100, digits=3), " % variance"))



#CELL
model_pca_cell <- prcomp(cell_traits[, c(model_rf_cell$`_selected_variables_`)], scale=TRUE, center=TRUE)
#model_pca <- prcomp(leaf_traits[, c("LLSH", "MTC", "LDMC", "DSLM", "VPL")], scale=TRUE, center=TRUE)

# ggplot
autoplot(model_pca_cell, data=cell_traits, size=3, color=species_colors_samples_cell,
         loadings=TRUE, loadings.color="black",
         loadings.label=TRUE, loadings.label.hjust=1, loadings.label.vjust=1, loadings.label.repel=TRUE, loadings.label.size=4, loadings.label.color="black" ) +
  theme(panel.grid.minor=element_line(color="lightgrey", size=0.25, linetype=3),
        panel.grid.major=element_line(color="grey", size=0.5, linetype=3),
        panel.background=element_blank(),
        panel.border=element_rect(color="black", fill=NA, size=1) ) +
  scale_color_manual(values=as.character(species_colors_samples_cell), labels=gsub(x=species_colors_samples_cell, pattern="\\.", replacement="\\. ")) +
  scale_fill_manual(values=as.character(species_colors_samples_cell)) +
  guides(shape=guide_legend(override.aes=list(size=2))) +
  theme(legend.position='bottom', legend.direction='vertical', plot.title=element_text(hjust=0.5), axis.title = element_text(size = 13), axis.text = element_text(size = 12)) +
  labs(title="PCA des signifikantesten Zelleigenschaften", title.fontface="bold", x=paste0("PC1: ", format(summary(model_pca_cell)$importance[2, 1] * 100, digits=3), " % variance"), y=paste0("PC2: ", format(summary(model_pca_cell)$importance[2, 2] * 100, digits=3), " % variance"))






#not working


# ---------- RDA ----------
# Format BET data matrix
bet_species <- rbind(bet_species[1:5,], bet_species[5,], bet_species[6:7,])
bet_species$friendly_name <- c("B. rutabulum", "G. pulvinata", "H. lutescens", "H. cupressiforme", "P. undulatum (f)", "P. undulatum (m)", "Bryum sp.", "R. squarrosus")

# Replicate species according to each sample
bet_traits <- data.frame()
for (i in 1:nrow(leaf_traits)) {
	bet_traits <- rbind(bet_traits, bet_species[which(species_samples_leaf[i] == bet_species$friendly_name), ])
}
bet_traits <- as.data.frame(bet_traits)

# Only take life-history traits
#bet_traits <- bet_traits[, c(11:15,21:25)]

# Only take bioclimatic traits
bet_traits <- bet_traits[, c(76:93)]

# Make numeric each column
for (i in 1:ncol(bet_traits)) {
	if (! any(is.na(as.numeric(bet_traits[, i])))) {
		bet_traits[, i] <- abs(as.numeric(bet_traits[, i]))
	} else {
		bet_traits[, i] <- as.numeric(as.factor(bet_traits[, i]))
	}
}
bet_traits[is.na(bet_traits)] <- 0

# Remove columns with constant values
#bet_traits <- bet_traits[,apply(bet_traits, 2, var, na.rm=TRUE) != 0]

# Scale matrix
bet_traits <- as.data.frame(scale(bet_traits, scale=TRUE, center=FALSE))

# Create formula
attach(bet_traits)
bet_traits_rda_formula <- formula(paste0("~ 0 + ", paste0(colnames(bet_traits),collapse=" + ")))
bet_traits_rda_y <- data.frame(model.matrix(bet_traits_rda_formula))
detach(bet_traits)

# Calculate overlay of descriptors on leaf traits distances
model_leaf_traits_dbrda <- dbrda(formula=scale(leaf_traits[,8:36]) ~ ., data=bet_traits_rda_y, distance="euclidian", metaMDSdist=FALSE, add=TRUE, sqrt.dist=FALSE)
model_leaf_traits_dbrda_scores <- vegan::scores(model_leaf_traits_dbrda)
model_leaf_traits_dbrda_ef_descriptors <- envfit(model_leaf_traits_dbrda, bet_traits, perm=10000)

# Goodness of fit statistic: Squared correlation coefficient
model_leaf_traits_dbrda_fit_descriptors <- data.frame(r2=c(model_leaf_traits_dbrda_ef_descriptors$vectors$r,model_leaf_traits_dbrda_ef_descriptors$factors$r),
													  pvals=c(model_leaf_traits_dbrda_ef_descriptors$vectors$pvals,model_leaf_traits_dbrda_ef_descriptors$factors$pvals) )
rownames(model_leaf_traits_dbrda_fit_descriptors) <- c(names(model_leaf_traits_dbrda_ef_descriptors$vectors$r),names(model_leaf_traits_dbrda_ef_descriptors$factors$r))
model_leaf_traits_dbrda_fit_descriptors
#write.csv(model_leaf_traits_dbrda_fit_descriptors, file="leaf_traits_dbrda_fit.csv", row.names=TRUE)

# Plot dbRDA
plot(model_leaf_traits_dbrda_scores$sites[,c(1:2)],
	 xlim=c(min(model_leaf_traits_dbrda_scores$sites[,1])-1, max(model_leaf_traits_dbrda_scores$sites[,1])+1),
	 ylim=c(min(model_leaf_traits_dbrda_scores$sites[,2]), max(model_leaf_traits_dbrda_scores$sites[,2])),
	 xlab=paste0("dbRDA1 (",round(as.data.frame(summary(model_leaf_traits_dbrda)$cont$importance)["Proportion Explained",c(1)]*100,2),"%)"),
	 ylab=paste0("dbRDA2 (",round(as.data.frame(summary(model_leaf_traits_dbrda)$cont$importance)["Proportion Explained",c(2)]*100,2),"%)"),
	 pch=19, col=species_colors_samples_leaf,
	 main="dbRDA der bioklimatischen Eigenschaften")
legend("bottomleft", bty="n", legend=species, pch=19, col=species_colors, pt.cex=1.4, cex=1, y.intersp=0.8, text.width=0.1)

#text(model_leaf_traits_dbrda_scores$sites[,c(1:2)], display="sites", labels=rownames(leaf_traits), col=species_colors_samples_leaf, pos=3, cex=0.5)
plot(model_leaf_traits_dbrda_ef_descriptors, cex=0.9, p.max=1, col="black")



# Model with intercept only
model_0_leaf_traits_rda <- vegan::dbrda(formula=scale(leaf_traits[,8:36]) ~ 1, data=bet_traits_rda_y, distance="euclidian", metaMDSdist=FALSE, add=TRUE, sqrt.dist=FALSE)

# Model with all explanatory variables
model_1_leaf_traits_rda <- vegan::dbrda(formula=scale(leaf_traits[,8:36]) ~ ., data=bet_traits_rda_y, distance="euclidian", metaMDSdist=FALSE, add=TRUE, sqrt.dist=FALSE)

# Stepwise forward selection
model_step_leaf_traits_rda <- ordistep(object=model_0_leaf_traits_rda, scope=formula(model_1_leaf_traits_rda), R2scope=TRUE, trace=TRUE, Pin=0.05, Pout=0.5, direction="forward", perm.max=10000)
model_step_leaf_traits_rda_scores <- vegan::scores(model_step_leaf_traits_rda)

# dbRDA with selected model by permutation tests in constrained ordination
model_leaf_traits_rda <- vegan::dbrda(formula=as.formula(model_step_leaf_traits_rda$terms), data=bet_traits_rda_y, distance="euclidian", metaMDSdist=FALSE, add=TRUE, sqrt.dist=FALSE)
model_leaf_traits_rda_ef_formula <- update(as.formula(model_step_leaf_traits_rda$terms), model_leaf_traits_rda ~ .)
model_leaf_traits_rda_ef_factors <- as.factor(sapply(strsplit(as.character(model_leaf_traits_rda_ef_formula)[[3]], "\\+"), function(x) { x <- gsub("(\\`|^ | $)","",x) }))
model_leaf_traits_rda_ef <- envfit(formula=model_leaf_traits_rda_ef_formula, data=bet_traits_rda_y, choices=c(1:2), perm=10000)
model_leaf_traits_rda_scores <- vegan::scores(model_leaf_traits_rda, choices=c(1:2))

# Goodness of fit statistic: Squared correlation coefficient
model_leaf_traits_rda_fit <- data.frame(r2=c(model_leaf_traits_rda_ef$vectors$r,model_leaf_traits_rda_ef$factors$r),
										pvals=c(model_leaf_traits_rda_ef$vectors$pvals,model_leaf_traits_rda_ef$factors$pvals) )
rownames(model_leaf_traits_rda_fit) <- c(names(model_leaf_traits_rda_ef$vectors$r),names(model_leaf_traits_rda_ef$factors$r))
model_leaf_traits_rda_fit
#write.csv(model_leaf_traits_rda_fit, file="plots_species/descriptors_bina_list_dbrda_sel_fit.csv", row.names=TRUE)

# Plot dbRDA
plot(model_leaf_traits_rda_scores$sites[,c(1:2)],
	 xlim=c(min(model_leaf_traits_rda_scores$sites[,1])-1, max(model_leaf_traits_rda_scores$sites[,1])+1),
	 ylim=c(min(model_leaf_traits_rda_scores$sites[,2]), max(model_leaf_traits_rda_scores$sites[,2])),
	 xlab=paste0("dbRDA1 (",round(as.data.frame(summary(model_leaf_traits_rda)$cont$importance)["Proportion Explained",c(1)]*100,2),"%)"),
	 ylab=paste0("dbRDA2 (",round(as.data.frame(summary(model_leaf_traits_rda)$cont$importance)["Proportion Explained",c(2)]*100,2),"%)"),
	 pch=19, col=species_colors_samples_leaf,
	 main="dbRDA der bioklimatischen Eigenschaften")
#text(model_leaf_traits_rda_scores$sites[,c(1:2)], display="sites", labels=rownames(leaf_traits), col=species_colors_samples_leaf, pos=3, cex=0.5)
plot(model_leaf_traits_rda_ef, cex=0.75, p.max=1, col="black")



# ---------- Phylogeny Tree ----------
#install.packages("rotl")
library(rotl)

# Search open tree of life for species names
taxa <- tnrs_match_names(names=c("Brachythecium rutabulum", "Hypnum cupressiforme", "Grimmia pulvinata", "Rhytidiadelphus squarrosus", "Plagiomnium undulatum", "Bryum capillare", "Homalothecium lutescens"))

# Build phylogenetic tree
tree <- tol_induced_subtree(ott_ids=ott_id(taxa))

# Plot phylogenetic tree
plot(tree, cex=0.8, label.offset=0.1, no.margin=TRUE)

# Make matrix with mean values of leaf traits
leaf_traits_phylo <- as.data.frame(leaf_traits[1:2,])
for (i in species) {
	leaf_traits_phylo <- rbind(leaf_traits_phylo, apply(leaf_traits[species_samples_leaf==species[species==i], ], 2, median))
}
leaf_traits_phylo <- leaf_traits_phylo[-c(1,2),]
rownames(leaf_traits_phylo) <- species
leaf_traits_phylo <- leaf_traits_phylo[-2,] # Remove male Plagiomnium

# Plot leaf traits tree
plot(as.phylo(hclust(dist(leaf_traits_phylo, method="euclidean"), method="complete")), direction="leftwards")

# Plot side by side
par(mfrow=c(1,2), mar=c(1,1,1,1), oma=c(0,0,0,0), cex.axis=0.9, cex=0.8)
plot(tree, cex=0.8, label.offset=0.1, no.margin=TRUE)
plot(as.phylo(hclust(dist(leaf_traits_phylo, method="euclidean"), method="complete")), direction="leftwards")


