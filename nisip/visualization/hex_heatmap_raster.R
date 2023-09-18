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
heatmap_matrix <- read.csv(file_path, header = FALSE)

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
          col = col, border = "green")
}

x <- as.vector(as.matrix(heatmap_matrix))

height <- dim(heatmap_matrix)[1]
width <- dim(heatmap_matrix)[2]

# output_path <- "heatmap_R.png"

png(output_path, width = width * 150, height = height * 150, res = 100)

par(mar = c(0.4, 2, 2, 7))

plot(0, 0, type = "n", axes = FALSE,
     xlim = c(0, width),
     ylim = c(0, height),
     xlab = "", ylab = "", asp = 1)

col_ramp <- rev(viridis(50, option = "magma"))
# color_code <- rep("#FFFFFF", length(x)) #default is all white

# bins <- seq(min(x, na.rm = TRUE), max(x, na.rm = TRUE),
#             length = length(col_ramp))
# for (i in seq_along(x)){
#   if (!is.na(x[i])) color_code[i] <- col_ramp[which.min(abs(bins - x[i]))]
# }
num_colors <- 6
# B <- viridis(num_colors)[heatmap_matrix + 1, ]
color_palette <- colorRampPalette(viridis(num_colors))
B <- color_palette(num_colors + 1)[heatmap_matrix + 1]
print(B)



# offset <- 0.5
offset <- 0
print(height)
print("width")
for (row in 0:(height-1)) {
  for (column in 0:(width-1)){
    hexagon(column + offset, row, col = B[row, column])
  }
  # offset <- ifelse(offset, 0, 0.5)
  offset <- offset + 0.5
}

dev.off()
