const img_vistpevia=document.getElementById("img_preview");

const img_cargando=document.getElementById("img-uploader");
const  CLOUDINARY_URL='https://api.cloudinary.com/v1_1/vale3443/image/upload'
const CLOUDINARY_UPLOAD_PRESENT="puiutrqn"
ImageUploader.addEventListener('change', async  (e) => {
    const file =e.target.files[0];

    const formData= new FormDfata();
    formData.append('file',file);
    //si sequiere que solo suba usuario cod
     formData.append('upload_preset',CLOUDINARY_UPLOAD_PRESENT)

    const res= await axios.post(CLOUDINARY_URL ,formData, {
        headers:{
            'content-tipe': 'multipart/form-data'
        }
    });
    console.log(res);
    imp_preview.src=res.data.secure_url;
   
});

var publi=[];
