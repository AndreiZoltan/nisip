library(reticulate)
library(viridis)
library(viridisLite)
use_python("/home/zoltan/miniconda3/envs/nis/bin/python")
my_data <- py_load_object("./random.pkl")
library(RColorBrewer) #to use brewer.pal
# library(fields)
hexagon <- function(x, y, unitcell = 1, col = col) {
  polygon(c(x, x, x + unitcell / 2, x + unitcell, x + unitcell,
            x + unitcell / 2), c(y + unitcell * 0.125,
                                 y + unitcell * 0.875,
                                 y + unitcell * 1.125,
                                 y + unitcell * 0.875,
                                 y + unitcell * 0.125,
                                 y - unitcell * 0.125),
          col = col, border = NA)
}#function
library(reticulate)
Heatmap_Matrix <- py_load_object("./random.pkl")
x <- as.vector(Heatmap_Matrix)
head(x)
SOM_Rows <- dim(Heatmap_Matrix)[1]
SOM_Columns <- dim(Heatmap_Matrix)[2]
par(mar = c(0.4, 2, 2, 7))
plot(0, 0, type = "n", axes = FALSE, xlim=c(0, SOM_Columns),
     ylim=c(0, SOM_Rows), xlab="", ylab= "", asp=1)

ColRamp <- rev(viridis(50, option = "magma"))
ColorCode <- rep("#FFFFFF", length(x))
Bins <- seq(min(x, na.rm=T), max(x, na.rm=T), length=length(ColRamp))
for (i in 1:length(x))
  if (!is.na(x[i])) ColorCode[i] <- ColRamp[which.min(abs(Bins-x[i]))]
offset <- 0.5 #offset for the hexagons when moving up a row
for (row in 1:SOM_Rows) {
  for (column in 0:(SOM_Columns - 1))
    hexagon(column + offset, row - 1, col = ColorCode[row + SOM_Rows * column])
  offset <- ifelse(offset, 0, 0.5)
}


# Create a legend for the custom color palette ColRamp
legend.only <- TRUE
col <- ColRamp
zlim <- c(min(x, na.rm = TRUE), max(x, na.rm = TRUE))

# Calculate the color breakpoints
breaks <- seq(zlim[1], zlim[2], length.out = length(col) + 1)

# Create legend labels (you can adjust these labels as needed)
labels <- format(breaks[-1], scientific = FALSE, trim = TRUE)

# Plot the legend
legend("topright", legend = labels, fill = col, title = "Legend Title", title.adj = 0.5,
       border = "black", bty = "n", cex = 0.8)
# dev.off()
# Save the plot to a PNG file in current working directory
current_dir <- getwd()

# png("heatmap_legend.png", width = 6, height = 4, units = "in", res = 300) # Adjust width, height, and resolution as needed
# par(mar = c(5, 5, 4, 2))  # Adjust margins as needed for your plot

# # Create a blank plot for the legend (you can adjust the dimensions as needed)
# plot.new()
# legend.only <- TRUE
# col <- ColRamp
# zlim <- c(min(x, na.rm = TRUE), max(x, na.rm = TRUE))

# # Calculate the color breakpoints
# breaks <- seq(zlim[1], zlim[2], length.out = length(col) + 1)

# # Create legend labels (you can adjust these labels as needed)
# labels <- format(breaks[-1], scientific = FALSE, trim = TRUE)

# # Plot the legend
# legend("topright", legend = labels, fill = col, title = "Legend Title", title.adj = 0.5,
#        border = "black", bty = "n", cex = 0.8)

# # Close the PNG device
# dev.off()