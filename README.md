Steps to run:

Open the folder in an IDE (Eg: VScode)

Backend:

1. Navigate to the backend folder -> cd backend
<!-- Create a virtual env (Optional) -->
2. RUN the command -> pip install -r requirements.txt
3. RUN the command python ./app.py

<!-- Service should be running on localhost:5000 -->

Frontend:

1. Navigate to the frontend folder -> cd frontend
2. RUN the command -> npm i
   Once the above execution is complete,
3. RUN the command -> npm run dev

<!-- UI should be running on localhost:5173 -->

Use the upload button to upload a pdf and view its content.
Use the Clear button to clear the content once a file is uploaded.(Optional)

<!--  -->

For only generating the output text file, please run the file - extract_pdf.py (python ./extract_pdf).
The output file will be created in output.txt as the input pdf is already present in the backend directory.

Running the process via API/Frontend will save any uploaded pdfs in a folder and also the converted text files in another separate folder.

Already placed the text output for the given pdf in a folder called "text-output" in the backend directory.

Nearly all steps in the assigned task has been completed. Few things like formatting, and recognising bullets embedded in paragraphs could be enhanced further. Formatting code is written taking the provided input PDF as reference, can be generalised for pdf documents containing text.

Referred to the internet for assistance in formatting, especially in regex patterns.

 <!--  -->
