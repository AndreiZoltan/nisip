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
  # polygon(c(x,
  #           x,
  #           x + unitcell / 2,
  #           x + unitcell,
  #           x + unitcell,
  #           x + unitcell / 2),
  #         c(y + unitcell * 0.125,
  #           y + unitcell * 0.875,
  #           y + unitcell * 1.125,
  #           y + unitcell * 0.875,
  #           y + unitcell * 0.125,
  #           y - unitcell * 0.125),
  #         col = col, border = FALSE)
  h <- sqrt(3) / 2 * unitcell
  polygon(c(x,
            x + unitcell / 2,
            x + unitcell,
            x + unitcell,
            x + unitcell / 2,
            x),
          c(y - h / 2,
            y - h,
            y - h / 2,
            y + h / 2,
            y + h,
            y + h / 2),
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

# png(output_path, width = cols * 140, height = rows * 90, res = 100)
input_height <- rows
input_width <- 3*cols/2
if (input_height > input_width) {
  png(output_path, width = input_width*2000/input_height, height = 2000, res = 100)
} else {
  png(output_path, width = 2000, height = input_height*2000/input_width, res = 100)
}
# png(output_path, width = 2000, height = 2000, res = 100)

par(mar = c(0.4, 2, 2, 7))
unitcell <- 1
plot(0, 0, type = "n", axes = FALSE,
     xlim = c(0, 3*cols*unitcell/2),
     ylim = c(-rows*unitcell, 0),
     xlab = "", ylab = "", asp = 1)
# plot(0, 0, type = "n", axes = FALSE,
#      xlim = c(0, cols),
#      ylim = c(-rows, 0),
#      xlab = "", ylab = "", asp = 1)

col_ramp <- rev(viridis(50, option = "magma"))
num_colors <- 6
heatmap_matrix <- matrix2color(heatmap_matrix, colormap = "viridis")

# unitcell <- 1
offset <- 0
for (row in rows:1) {
  for (column in 1:cols){
    x <- column * unitcell + offset
    y <- row * (sqrt(3) / 2 * unitcell)
    hexagon(x, -y, col = heatmap_matrix[row, column], unitcell = unitcell)
  }
  offset <- offset + unitcell / 2
}

# offset <- 0
# for (row in rows:1) {
#   for (column in 1:cols){
#     x <- column + offset
#     y <- row
#     hexagon(x, -y, col = heatmap_matrix[row, column])
#   }
#   offset <- offset + 0.5
# }

dev.off()
