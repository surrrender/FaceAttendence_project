<template>
  <div class="container">
    <el-input
      v-model="lectureName"
      style="width: 240px"
      size="large"
      placeholder="请输入班级的课程名称"
    />
    <el-upload
      class="upload-demo"
      drag
      :http-request="customUpload"
      action="https://run.mocky.io/v3/9d059bf9-4660-45f2-925d-ce80ad6c4d15"
      multiple
      @success="handleSuccess"
      @error="handleError"
    >
      <el-icon class="el-icon--upload"><upload-filled /></el-icon>
      <div class="el-upload__text">Drop file here or <em>click to upload</em></div>
      <template #tip>
        <div class="el-upload__tip">jpg/png files with a size less than 500kb</div>
      </template>
    </el-upload>

    <el-dialog
      class="dialog"
      v-model="dialogVisible"
      width="480"
      :modal="false"
      align-center
    >
      <!-- 展示当前人脸 -->
      <img :src="currentFace" alt="Face" v-if="currentFace" class="centered-image" />

      <!-- 输入人名的表单 -->
      <el-input v-model="enteredName" placeholder="请输入人名"></el-input>

      <!-- 确认和取消按钮 -->
      <span slot="footer" class="dialog-footer">
        <el-button @click="cancelSubmit">取 消</el-button>
        <el-button type="primary" @click="submit">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script setup>
import { UploadFilled } from "@element-plus/icons-vue";
import { ref } from "vue";
import axios from "axios";
import { decode } from "base-64";

const faceEncodings = ref([]); // 存储从后端返回的人脸编码

let names = []; // 存储用户输入的姓名
const faceLocations = ref([]); // 存储照片位置
const base64Image = ref(""); // 存储在前端的照片
const croppedFaceImage = ref(""); // 存储裁剪后的人脸图片

const save_path = ref(); //图片在后端的存储位置
const currentFace = ref(""); //当前人脸的数据
const enteredName = ref(""); //当前人脸的姓名
const currentFaceIndex = ref(0);

const dialogVisible = ref(false);

const lectureName = ref("");

const baseURL = import.meta.env.VITE_API_BASE_URL;
const customUpload = async (options) => {
  const { file } = options;
  try {
    // 使用FileReader将文件转换为Base64编码
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onloadend = () => {
      base64Image.value = reader.result; // 存储Base64编码的图片
      // 在这里可以进行展示图片的操作，例如更新Vue组件的数据
      console.log("Base64 Image:", base64Image);
    };

    const formData = new FormData();
    formData.append("file", file);
    formData.append("lecture_name", lectureName.value);
    const token = localStorage.getItem("token");
    console.log(token);
    const response = await axios.post(`${baseURL}FA/detect_face/`, formData, {
      headers: {
        "Content-Type": "multipart/form-data",
        Authorization: `Token ${token}`,
      },
    });
    console.log("Upload success:", response.data.message);
    // console.log("savepath",response.data.save_path);
    save_path.value = response.data.save_path;
    faceLocations.value = response.data.face_locations;
    // cropFace();
    startFacePresentation();

    //上传成功后的处理
    // requireAllNames(faceEncodings);
  } catch (error) {
    options.onError(error);
  }
};

const startFacePresentation = () => {
  currentFaceIndex.value = 0;
  showTheSingleFace(currentFaceIndex.value);
};

const showTheSingleFace = (faceIndex) => {
  console.log(faceLocations.value.length);
  if (currentFaceIndex.value < faceLocations.value.length) {
    //展示人脸照片
    const img = new Image();
    img.src = base64Image.value;
    img.onload = () => {
      // 创建 canvas 上下文
      const canvas = document.createElement("canvas");
      const ctx = canvas.getContext("2d");

      //这里应该写一个循环，遍历所有的人脸，每次开始执行的条件是点击了submit按钮

      const face = faceLocations.value[faceIndex]; // 假设我们只处理第一张脸
      ctx.drawImage(
        img,
        face[3],
        face[0],
        face[1] - face[3],
        face[2] - face[0],
        0,
        0,
        face[1] - face[3],
        face[2] - face[0]
      );
      currentFace.value = canvas.toDataURL();
      // console.log(currentFace.value);
      // croppedFaceImage.value = canvas.toDataURL();
      dialogVisible.value = true;
    };
  } else {
    //人脸识别完毕
    dialogVisible.value = false;
    currentFaceIndex.value = 0; // 重置索引，以便下次重新开始
    //在这里写上给后端一次性发送所有locaiton和name的代码
    console.log(names);
    sendFaceAccordingNames();
    names = [];
    lectureName.value='';
  }
};

const submit = () => {
  //发送数据给后端
  //清空输入人名
  names.push(enteredName.value);
  console.log("人名:", names);
  enteredName.value = "";

  //展示下一个人脸
  currentFaceIndex.value++;
  showTheSingleFace(currentFaceIndex.value);
};

// 发送人脸位置和姓名给后端
const sendFaceAccordingNames = async () => {
  const face_locations = faceLocations.value;
  const face_names = names;
  console.log(lectureName.value);

  const data = {
    face_locations: face_locations,
    names: face_names,
    save_path: save_path.value,
    lecture_name: lectureName.value,
  };

  console.log(data);
  const jsonData = JSON.stringify(data);
  const token = localStorage.getItem("token");
  // 发送到后端
  const response = await axios.post(`${baseURL}FA/save_face_encoding/`, jsonData, {
    headers: {
      "Content-Type": "application/json",
      Authorization: `Token ${token}`,
    },
  });
  console.log(response);
};

const cancelSubmit = () =>{
  dialogVisible.value = false;
  names = [];
}
</script>

<style>
.upload-demo {
  /* display: flex;
    flex-direction: column; */
  width: 1000px;
}
.el-icon--upload {
  height: 500px;
}
.dialog {
  display: flex;
  flex-direction: column;
  /* justify-content: center; */
  align-items: center;
  height: 100%; /* 确保容器高度填满对话框 */
}

.centered-image {
  max-width: 400px; /* 设置图片最大宽度为400px */
  width: 80%; /* 让图片宽度占满容器 */
  height: auto; /* 保持图片宽高比 */
}

.dialog-footer {
  margin-top: 20px;
}
</style>
