<template>
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

    <!-- <img v-if="croppedFaceImage" :src="croppedFaceImage" alt="Cropped Face Image" /> -->
    <!-- <div v-if="face_locations.length > 0">
      <div v-for="(face_location, index) in face_locations" :key="index">
        <p>
          Face {{ index + 1 }} - Location: Top: {{ face_location[1] }}, Right:
          {{ face_location[3] }}, Bottom: {{ face_location[2] }}, Left:
          {{ face_location[0] }}
        </p>
        <canvas
          :id="'canvas' + index"
          :width="face_location[1] - face_location[3]"
          :height="face_location[2] - face_location[0]"
        ></canvas>
      </div>
    </div> -->
  </el-upload>
  <!-- 展示识别到的人脸编码 -->
  <!-- <div v-for="(encoding, index) in faceEncodings" :key="index">
    <img :src="getFaceImage(encoding)" alt="Face" />
    <input v-model="names[index]" placeholder="Enter Name" />
    <el-button @click="sendFaceData(index)">Submit</el-button>
  </div> -->
  <!-- <img v-if="base64Image" :src="base64Image" alt="Uploaded Image" /> -->

  <img v-if="croppedFaceImage" :src="croppedFaceImage" alt="Cropped Face Image" />
  <el-dialog
    class="dialog"
    v-model="dialogVisible"
    width="480"
    :modal="false"
    align-center
  >
    <!-- 展示当前人脸 -->
    <img :src="currentFace" alt="Face" v-if="currentFace" />

    <!-- 输入人名的表单 -->
    <el-input v-model="enteredName" placeholder="请输入人名"></el-input>

    <!-- 确认和取消按钮 -->
    <span slot="footer" class="dialog-footer">
      <el-button @click="dialogVisible = false">取 消</el-button>
      <el-button type="primary" @click="submit">确 定</el-button>
    </span>
  </el-dialog>
</template>

<script setup>
import { UploadFilled } from "@element-plus/icons-vue";
import { ref } from "vue";
import axios from "axios";
import { decode } from "base-64";

const faceEncodings = ref([]); // 存储从后端返回的人脸编码
const names = ref([]); // 存储用户输入的姓名
const faceLocations = ref([]); // 存储照片位置
const base64Image = ref(""); // 存储在前端的照片
const croppedFaceImage = ref(""); // 存储裁剪后的人脸图片

const save_path = ref();
const currentFace = ref("");
const enteredName = ref('');
const currentFaceIndex = ref(0);

const dialogVisible = ref(true);

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

    const response = await axios.post(`${baseURL}FA/detect_face/`, formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
    console.log("Upload success:", response.data.message);
    console.log("savepath",response.data.save_path);
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
  cropFace(currentFaceIndex.value);
};

const cropFace = (faceIndex) => {
  console.log(faceLocations.value.length)
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
      console.log(currentFace.value);
      // croppedFaceImage.value = canvas.toDataURL();
      dialogVisible.value = true;
    };
  } else {
    //人脸识别完毕
    dialogVisible.value = false;
    currentFaceIndex.value = 0;// 重置索引，以便下次重新开始
    //在这里写上给后端一次性发送所有locaiton和name的代码
    sendFaceData();
    names.value.length = 0;
  }
};

const submit = () => {
  //发送数据给后端
  //清空输入人名
  names.value.push(enteredName.name);
  enteredName.value = '';
  //展示下一个人脸
  currentFaceIndex.value++;
  cropFace(currentFaceIndex.value);
};

const requireAllNames = (face_encodings) => {
  for (const face_encoding of face_encodings) {
  }

  imageUrl.value = URL.createObjectURL(file); // 显示上传的图片
};


// 发送人脸位置和姓名给后端
const sendFaceData = async () => {
  const face_locations = faceLocations.value;
  const face_names = names.value;

  const data = { face_locations:face_locations, names : face_names, save_path:save_path};
  const jsonData = JSON.stringify(data);
  // 发送到后端
  const response = await axios.post(`${baseURL}FA/save_face_encoding/`, jsonData, {
    headers: {
      "Content-Type": "application/json",
    },
  });
  console.log(response);
};
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
</style>
