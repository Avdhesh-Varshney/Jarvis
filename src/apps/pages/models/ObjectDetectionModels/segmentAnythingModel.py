import streamlit as st
import tensorflow as tf
from transformers import TFSamModel, SamProcessor
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

# Enable numpy behavior
tf.experimental.numpy.experimental_enable_numpy_behavior()

@st.cache_resource
def load_model():
    """Load the SAM model and processor."""
    model = TFSamModel.from_pretrained("facebook/sam-vit-base")
    processor = SamProcessor.from_pretrained("facebook/sam-vit-base")
    return model, processor

def generate_random_colors(n):
    """Generate n distinct colors."""
    colors = []
    for i in range(n):
        # Generate bright, distinct colors
        hue = i / n
        saturation = 0.7 + np.random.rand() * 0.3
        value = 0.7 + np.random.rand() * 0.3
        
        # Convert HSV to RGB
        h = hue * 6
        c = value * saturation
        x = c * (1 - abs(h % 2 - 1))
        m = value - c
        
        if h < 1:
            rgb = (c, x, 0)
        elif h < 2:
            rgb = (x, c, 0)
        elif h < 3:
            rgb = (0, c, x)
        elif h < 4:
            rgb = (0, x, c)
        elif h < 5:
            rgb = (x, 0, c)
        else:
            rgb = (c, 0, x)
            
        colors.append(np.array([(r + m) * 0.7 for r in rgb] + [0.5]))  # Add alpha value
    return colors

def show_masks_on_image(raw_image, masks, scores):
    """Display all masks overlaid on the same image with different colors."""
    plt.clf()
    
    # Convert tensors to numpy arrays
    if isinstance(masks, tf.Tensor):
        masks = masks.numpy()
    if isinstance(scores, tf.Tensor):
        scores = scores.numpy()
    
    masks = np.squeeze(masks)
    scores = np.squeeze(scores)
    
    # Handle single mask case
    if len(masks.shape) == 2:
        masks = np.expand_dims(masks, 0)
        scores = np.expand_dims(scores, 0)
    
    # Create figure
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.imshow(raw_image)
    
    # Generate distinct colors for each mask
    colors = generate_random_colors(len(masks))
    
    # Overlay each mask with a different color
    for i, (mask, score, color) in enumerate(zip(masks, scores, colors)):
        # Show masked image
        mask_image = np.zeros((mask.shape[0], mask.shape[1], 4))
        mask_image[:, :, 3] = mask * color[3]  # Alpha channel
        for j in range(3):  # RGB channels
            mask_image[:, :, j] = mask * color[j]
        
        ax.imshow(mask_image)
        
        # Add label with score
        label = f"Object {i+1} (Score: {float(score):.2f})"
        # Find center of mass of the mask for label placement
        y_indices, x_indices = np.where(mask > 0.5)
        if len(x_indices) > 0 and len(y_indices) > 0:
            center_x = np.mean(x_indices)
            center_y = np.mean(y_indices)
            ax.text(center_x, center_y, label, 
                   color='white', fontsize=8, 
                   bbox=dict(facecolor='black', alpha=0.5),
                   ha='center', va='center')
    
    ax.axis('off')
    plt.tight_layout()
    return fig

def segmentAnythingModel():
    st.title("Segment Anything Model (SAM)")
    st.write("""
    Upload an image to automatically segment all objects in the scene. 
    Each object will be highlighted with a different color.
    """)

    # Load model at the start
    with st.spinner("Loading model..."):
        try:
            model, processor = load_model()
            st.success("Model loaded successfully!")
        except Exception as e:
            st.error(f"Error loading model: {str(e)}")
            return

    # File uploader
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        try:
            # Display original image
            raw_image = Image.open(uploaded_file).convert("RGB")
            st.image(raw_image, caption="Original Image", use_column_width=True)
            
            # Generate grid of points across the image for complete segmentation
            height, width = raw_image.size[1], raw_image.size[0]
            grid_size = 50  # Adjust this value to control segmentation density
            x_points = np.linspace(0, width, num=grid_size)
            y_points = np.linspace(0, height, num=grid_size)
            
            input_points = [[[x, y] for x in x_points[::4] for y in y_points[::4]]]
            
            if st.button("Generate Segmentation"):
                with st.spinner("Generating segmentation..."):
                    try:
                        # Process the image with grid points
                        inputs = processor(raw_image, input_points=input_points, return_tensors="tf")
                        
                        # Run model inference
                        outputs = model(**inputs)
                        
                        # Post-process masks
                        masks = processor.image_processor.post_process_masks(
                            outputs.pred_masks,
                            inputs["original_sizes"],
                            inputs["reshaped_input_sizes"],
                            return_tensors="tf",
                        )
                        
                        # Create and display figure
                        fig = show_masks_on_image(raw_image, masks, outputs.iou_scores)
                        st.pyplot(fig)
                        plt.close(fig)
                        
                        st.success("Segmentation completed successfully!")
                        
                    except Exception as e:
                        st.error(f"Error during segmentation: {str(e)}")
                        st.write("Full error details:", e)

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.info("Please try again with a different image.")

if __name__ == "__main__":
    segmentAnythingModel()