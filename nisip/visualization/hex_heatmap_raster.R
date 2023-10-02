library(reticulate)
library(viridisLite)
library(viridis)
library(reticulate)
library(RColorBrewer)


args <- commandArgs(trailingOnly = TRUE)
file_path <- args[1]
output_path <- args[2]
print(file_path)
print(output_path)
heatmap_matrix <- read.csv(file_path, header = FALSE, sep = ",")
heatmap_matrix <- as.matrix(heatmap_matrix)

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
          col = col, border = FALSE)
}
matrix2color <- function(matrix, colormap = "viridis") {
  matrix <- as.matrix(matrix)
  col_ramp <- scales::col_numeric(colormap, domain = c(0, 1))  # Adjust domain to 0-1
  matrix <- (matrix - min(matrix, na.rm = TRUE)) / (max(matrix, na.rm = TRUE) - min(matrix, na.rm = TRUE))  # Scale to 0-1
  colors <- col_ramp(matrix)
  dim(colors) <- c(dim(matrix))
  return(colors)
}

matrix2color2 <- function(matrix, colormap = "viridis") {
  matrix <- as.matrix(matrix)
  col_ramp <- scales::col_numeric(colormap, domain = range(matrix))
  # matrix <- (matrix + 1) / 7
  matrix <- (matrix - min(matrix)) / diff(range(matrix))
  colors <- col_ramp(matrix)
  dim(colors) <- c(dim(matrix))
  return(colors)
}


rows <- dim(heatmap_matrix)[1]
cols <- dim(heatmap_matrix)[2]

png(output_path, width = cols * 150, height = rows * 150, res = 100)

par(mar = c(0.4, 2, 2, 7))

plot(0, 0, type = "n", axes = FALSE,
     xlim = c(-cols, 2*cols),
     ylim = c(-rows, rows),
     xlab = "", ylab = "", asp = 1)

col_ramp <- rev(viridis(50, option = "magma"))
num_colors <- 6
heatmap_matrix <- matrix2color(heatmap_matrix, colormap = "viridis")


offset <- 0
for (row in rows:1) {
  for (column in 1:cols){
    x <- column + offset
    y <- row
    hexagon(x, -y, col = heatmap_matrix[row, column])
  }
  offset <- offset + 0.5
}

dev.off()
