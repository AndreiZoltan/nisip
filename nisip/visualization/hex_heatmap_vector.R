library(reticulate)
library(viridisLite)
library(viridis)
library(reticulate)
library(RColorBrewer)
use_python("/home/zoltan/miniconda3/envs/nis/bin/python")
heatmap_matrix <- py_load_object("./random.pkl")

hexagon <- function(x, y, unitcell = 1, col = col) {
  polygon(c(x,
            x,
            x + unitcell / 2,
            x + unitcell,
            x + unitcell,
            x + unitcell / 2),
          c(y + unitcell * 0.125,
            y + unitcell * 0.875,
            y + unitcell * 1.125,
            y + unitcell * 0.875,
            y + unitcell * 0.125,
            y - unitcell * 0.125),
          col = col, border = NA)
}

x <- as.vector(heatmap_matrix)

SOM_Rows <- dim(heatmap_matrix)[1]
SOM_Columns <- dim(heatmap_matrix)[2]

output_path <- "heatmap_R.svg"

svg(output_path, width = 8, height = 8, pointsize = 12) # Adjust width, height, and pointsize as needed

par(mar = c(0.4, 2, 2, 7))

plot(0, 0, type = "n", axes = FALSE,
     xlim = c(0, SOM_Columns),
     ylim = c(0, SOM_Rows),
     xlab = "", ylab = "", asp = 1)

col_ramp <- rev(viridis(50, option = "magma"))
color_code <- rep("#FFFFFF", length(x)) #default is all white

bins <- seq(min(x, na.rm = TRUE), max(x, na.rm = TRUE),
            length = length(col_ramp))
for (i in seq_along(x)){
  if (!is.na(x[i])) color_code[i] <- col_ramp[which.min(abs(bins - x[i]))]
}

offset <- 0.5
for (row in 1:SOM_Rows) {
  for (column in 0:(SOM_Columns - 1)){
    hexagon(column + offset, row - 1, col = color_code[row + SOM_Rows * column])
  }
  offset <- ifelse(offset, 0, 0.5)
}

dev.off()