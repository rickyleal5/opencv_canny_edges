'''
Programmer: Ricardo A. Leal
Project: Use camera and apply Canny edge detection. The thresholds can be adjusted with trackbars.
			To save a picture, press 's'
'''

#Libraries
import cv2
import time

#Main
def main():
	#Get camera from computer
	cap = cv2.VideoCapture(0)

	#Create a window to display the camera frames
	cv2.namedWindow('camera')

	#Threshold trackbars
	cv2.createTrackbar('minValue', 'camera', 0, 500, do_nothing)
	cv2.createTrackbar('maxValue', 'camera', 0,500, do_nothing)

	#Error messages
	error_message1 = 'WARNING: maxVal should not be greater than minVal.'
	error_message2 = 'The program will swap their values until you fix them.'

	#Variables
	swap = False
	font = cv2.FONT_HERSHEY_SIMPLEX
	lineType = cv2.LINE_AA
	color = (255,255,255)
	fontScale = 0.7
	thickness = 1
	cam_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
	cam_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
	filename = ''

	#Show instruction to stop the program
	print("Press the 's' key to take a picture of the frame")
	print("Press the ESC key to exit the program")
	

	#Loop if the camera is open
	while(cap.isOpened()):
			#Read a frame
			ret, frame = cap.read()
			
			#Get trackbar values
			minVal = cv2.getTrackbarPos('minValue', 'camera')
			maxVal = cv2.getTrackbarPos('maxValue', 'camera')
			
			#Check if the user is not adjusting the thresholds properly
			if maxVal < minVal:
				#Show error messages
				print("\n", error_message1, "\n", error_message2)
				swap = True
				
				#Swap values
				temp = maxVal
				maxVal = minVal
				minVal = temp
				
			else:
				swap = False
		
			#Find edges using the Canny method
			canny = cv2.Canny(frame, threshold1 = minVal, threshold2 = maxVal)
			
			#Add error messages to the frame
			if swap == True:
				#Draw black rectangle
				canny = cv2.rectangle(canny, (0, 0), (cam_width, 60), (0,0,0), -1)
				#Add error messages to the frame
				cv2.putText(canny, error_message1, (0, 20), font, fontScale, color, thickness, lineType)
				cv2.putText(canny, error_message2, (0, 50), font, fontScale, color, thickness, lineType)
			
			#Display the frame
			cv2.imshow('camera', canny)
			
			#Take a picture if 's' is pressed
			if cv2.waitKey(1) & 0xFF == ord('s'):
				#Save picture
				filename = 'canny_{}.png'.format(str(time.time()).replace('.','_'))
				cv2.imwrite(filename, canny)
				print("Picture saved as ", filename)
			
			#Exit if ESC key is pressed
			if cv2.waitKey(1) & 0xFF == 27:
				cap.release()
	#Destroy all windows
	cv2.destroyAllWindows()

#Function 'do_nothing'. It is needed to create the trackbars
def do_nothing(x):
	pass

main()
