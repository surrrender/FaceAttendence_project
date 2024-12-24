<template>
  <div class="container">
    <div class="block">
      <!-- <span class="demonstration">Use value-format</span> -->
      <!-- <div class="demonstration">Value：{{ value2 }}</div> -->
      <el-date-picker
        v-model="value2"
        type="datetime"
        placeholder="请选择检查考勤的时间"
        format="YYYY/MM/DD hh:mm:ss"

      />
    </div>
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
      <div class="el-upload__text">拖动文件到这儿 or <em>点击上传文件</em></div>
      <template #tip>
        <div class="el-upload__tip">jpg/png files with a size less than 500kb</div>
      </template>
    </el-upload>
  </div>
</template>

<script setup>
import { UploadFilled } from "@element-plus/icons-vue";
import { ref } from "vue";
import axios from "axios";
import { decode } from "base-64";

const faceEncodings = ref([]); // 存储从后端返回的人脸编码
const currentFaceIndex = ref(0);

const dialogVisible = ref(false);
const absent_names = ref([]);
const value2 = ref("");

const baseURL = import.meta.env.VITE_API_BASE_URL;
const customUpload = async (options) => {
  const { file } = options;
  try {
    const formData = new FormData();
    formData.append("file", file);

    const response = await axios.post(`${baseURL}FA/check_attendance/`, formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
    console.log("Upload success:", response.data.message);
    absent_names.value = response.data.absent_names;
    console.log(absent_names.value);
  } catch (error) {
    options.onError(error);
  }
};
</script>

<style>
.container {
  display:flex;
  flex-direction: column;
}
.upload-demo {
  /* display: flex;
      flex-direction: column; */
  width: 1000px;
}
.el-icon--upload {
  height: 500px;
}
</style>
