import numpy as np
import math
import heapq
import matplotlib.pyplot as plt
import cv2
import io
class ImageSeg:
#Initializing the path of image and threshold value by taking as class parameters
    def __init__(self,path):
        self.path = path
        self.img = plt.imread(path)
        self.threshold = 0
    #Visualize the raw rgb image
    def visualize_rgb(self):
        rgb_img = self.img
        # plt.imshow(rgb_img)

    #Nullify the R and B values in the image matrix
    def RGNull(self):
        arr = np.array(self.img)
        greenval = 0
        count = 0
        for i in range(len(arr)):
            for j in range(len(arr[i])):
                count+=1
                greenval+=arr[i][j][1]
                arr[i][j][0]=0
                arr[i][j][2]=0
        self.threshold = (greenval/count)/1.5
        return arr

    #Grayscale the image
    def IsoGray(self):
        RGNull_img = self.RGNull()
        gray_img = cv2.cvtColor(RGNull_img,cv2.COLOR_RGB2GRAY)
        return gray_img

    #Apply Thresholding
    def IsoGrayThresh(self):

        gray_img = self.IsoGray()
        for i in range(len(gray_img)):
            for j in range(len(gray_img[i])):
                if gray_img[i][j]>self.threshold:
                    gray_img[i][j]=255
                else:
                    gray_img[i][j]=0

        # plt.imshow(gray_img)
        return gray_img

    #Comparison b/w raw rgb, grayscaled and thresholded images
    def visualize_compare(self):
        fig = plt.figure(figsize=(14, 30))
        row = 1
        cols = 3
        fig.add_subplot(row,cols,1)
        io.imshow(self.img)
        fig.add_subplot(row,cols,2)
        io.imshow(self.IsoGray())
        fig.add_subplot(row,cols,3)
        io.imshow(self.IsoGrayThresh())

    #Function to count the tree pixels in the thresholded image
    def PixelCount(self):
        count = 0
        arr = self.IsoGrayThresh()
        for i in arr:
            for j in i:
                if j!=0:
                    count+=1

        return count
class OptimalPathing:
    def __init__(self, img, PATH):
        self.img = img
        self.PATH = PATH

    def Precompute_EuclideanDist(self, img):
        rows, cols = len(img), len(img[0])
        AdjMat = np.zeros((rows, cols))
        for i in range(rows):
            for j in range(cols):
                AdjMat[i][j] = math.sqrt((i - (rows - 1)) ** 2 + (j - (cols - 1)) ** 2)
        return AdjMat

    def create_graph(self, binary_image, target):
        binary_image = np.array(binary_image)
        graph = {}
        rows, cols = len(binary_image), len(binary_image[0])
        TreeCount_Density = 115 / (rows * cols) * 1000     # Confidence_Val
        TCD_FACTOR = math.exp(TreeCount_Density * 100)
        AdjMat = self.Precompute_EuclideanDist(binary_image)
        for i in range(rows):
            for j in range(cols):
                neighbors = []
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if dx == 0 and dy == 0:
                            continue
                        ni, nj = i + dx, j + dy
                        if 0 <= ni < rows and 0 <= nj < cols:
                            euclid_dist = math.sqrt((ni - target[0]) ** 2 + (nj - target[1]) ** 2)
                            avg_density = 0
                            for fact in range(1, 11):
                                try:
                                    alpha_val = 255 - binary_image[ni - fact * dx][nj + fact * dy]
                                except:
                                    alpha_val = 0
                                try:
                                    beta_val = 255 - binary_image[ni + fact * dx][nj - fact * dy]
                                except:
                                    beta_val = 0
                                avg_density += alpha_val + beta_val

                            avg_density /= 20  # Average density over the 20 pixels
                            neighbors.append(((ni, nj), TCD_FACTOR * (255 - binary_image[ni][nj]) +
                                              euclid_dist ** 2 + 50000 * np.log(avg_density + 1)))

                graph[(i, j)] = neighbors  # Store the neighbors for the current pixel
        return graph

    def trace_path(self, parents, start, target):
        path = []
        current = target
        while current != start:
            path.append(current)
            current = parents[current]
        path.append(start)
        path.reverse()
        return path
    

    def ComputeAStar(self, start_pixel=(0, 0), target_pixel=(100, 200)):
        graph = self.create_graph(self.img, target_pixel)

        # Find the shortest path
        parents = {}
        heap = [(0, start_pixel)]
        visited = set()

        while heap:
            (cost, current) = heapq.heappop(heap)

            if current in visited:
                continue

            visited.add(current)

            if current == target_pixel:
                break

            for neighbor, weight in graph.get(current, []):
                if neighbor not in visited:
                    parents[neighbor] = current
                    heapq.heappush(heap, (cost + weight, neighbor))

        if target_pixel not in parents:
            print("Target pixel is unreachable.")
            return None, None

        shortest_path = self.trace_path(parents, start_pixel, target_pixel)

        # Visualize the image and the shortest path
        image = np.array(self.img)
        x_coords, y_coords = zip(*shortest_path)  # Extract x, y coordinates for plotting

        # Plot starting and ending points
        plt.plot(start_pixel[1], start_pixel[0], 'go')  # 'go' indicates green circle for start point
        plt.plot(target_pixel[1], target_pixel[0], 'ro')  # 'ro' indicates red circle for end point

        # Plot the path
        plt.plot(y_coords, x_coords, color='blue', linewidth=2)  # Plot the path in blue
        plt.imshow(plt.imread(self.PATH))

        # Save the plot as an in-memory image
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png')
        plt.close()  # Close the plot to free memory
        img_buffer.seek(0)

        # Processed Image (without plot)
        processed_image = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        _, processed_image = cv2.threshold(processed_image, 127, 255, cv2.THRESH_BINARY)

        return img_buffer,processed_image
# # Example usage:
# # Load an image using skimage.io.imread or any other method
# img = io.imread('path_to_your_image.jpg')
# obj = OptimalPathing(img)
# plot_image, processed_image = obj.ComputeAStar()

# Now you have two images: plot_image (original image with the plot) and processed_image (processed image)
# You can save or display these images as needed.
