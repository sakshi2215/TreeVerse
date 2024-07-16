import numpy as np
import math
import heapq
import matplotlib.pyplot as plt
import cv2
import io 
import base64
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
        rows, cols = img.shape
        AdjMat = np.fromfunction(lambda i, j: np.sqrt((i - (rows - 1)) ** 2 + (j - (cols - 1)) ** 2), (rows, cols))
        return AdjMat

    def create_graph(self, binary_image, target):
        binary_image = np.array(binary_image)
        rows, cols = binary_image.shape
        TreeCount_Density = 115 / (rows * cols) * 1000  # Confidence_Val
        TCD_FACTOR = math.exp(TreeCount_Density * 100)
        AdjMat = self.Precompute_EuclideanDist(binary_image)

        def compute_avg_density(ni, nj, dx, dy):
            alpha_vals = []
            beta_vals = []
            for fact in range(1, 4):
                if 0 <= ni - fact * dx < rows and 0 <= nj + fact * dy < cols:
                    alpha_vals.append(255 - binary_image[ni - fact * dx, nj + fact * dy])
                if 0 <= ni + fact * dx < rows and 0 <= nj - fact * dy < cols:
                    beta_vals.append(255 - binary_image[ni + fact * dx, nj - fact * dy])
            avg_density = (sum(alpha_vals) + sum(beta_vals)) / 20
            return avg_density

        graph = {}
        for i in range(rows):
            for j in range(cols):
                neighbors = []
                for dx, dy in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
                    ni, nj = i + dx, j + dy
                    if 0 <= ni < rows and 0 <= nj < cols:
                        euclid_dist = math.sqrt((ni - target[0]) ** 2 + (nj - target[1]) ** 2)
                        avg_density = compute_avg_density(ni, nj, dx, dy)
                        weight = TCD_FACTOR * (255 - binary_image[ni, nj]) + euclid_dist ** 2 + 50000 * np.log(avg_density + 1)
                        neighbors.append(((ni, nj), weight))
                graph[(i, j)] = neighbors
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

    def ComputeAStar(self, start_pixel=(0, 0), target_pixel=(645, 790)):
        graph = self.create_graph(self.img, target_pixel)
        parents = {}
        heap = [(0, start_pixel)]
        visited = set()

        while heap:
            cost, current = heapq.heappop(heap)

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
            return

        shortest_path = self.trace_path(parents, start_pixel, target_pixel)

        # Visualize the image and the shortest path
        image = np.array(self.img)
        x_coords, y_coords = zip(*shortest_path)  # Extract x, y coordinates for plotting
        # Convert grayscale to RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)

        thickness = 3  # You can adjust the thickness value as needed
        for i in range(len(x_coords) - 1):
            start_point = (y_coords[i], x_coords[i])
            end_point = (y_coords[i + 1], x_coords[i + 1])
            image_rgb = cv2.line(image_rgb, start_point, end_point, (255, 0, 0), thickness)

        return image_rgb
