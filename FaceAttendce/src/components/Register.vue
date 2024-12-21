<template>
  <div class="login-container">
    <el-card class="login-card">

      <h2 class="login-title">用户注册</h2>

      <el-form class="Form" :model="loginForm" :rules="rules" ref="loginFormRef" label-width="80px"
        label-position="left">

        <el-form-item label="用户名" prop="username">
          <el-input label="用户名" v-model="loginForm.username" placeholder="请输入用户名"></el-input>
        </el-form-item>

        <el-form-item label="密码" prop="password1">
          <el-input v-model="loginForm.password1" type="password" placeholder="请输入密码"></el-input>
        </el-form-item>

        <el-form-item label="确认密码" prop="password2">
          <el-input v-model="loginForm.password2" type="password" placeholder="请输入密码"></el-input>
        </el-form-item>

        <div class="below-buttons">
          <el-button class="RegisterButton" type="primary" @click="onSubmit">注册</el-button>
          <el-button class="RegisterButton" type="primary" @click="cancel">取消</el-button>
        </div>
      </el-form>
      <!-- <div class="below-buttons">
        <el-button class="RegisterButton" type="primary" @click="onSubmit">注册</el-button>
        <el-button class="RegisterButton" type="primary" @click="cancel">取消</el-button>
      </div> -->
    </el-card>
  </div>
</template>

<script>
import { defineComponent, reactive, ref } from 'vue';
import { ElForm, ElMessage, ElRow } from 'element-plus';
import axios from 'axios';
import { useRouter } from 'vue-router';

export default defineComponent({
  name: 'Register',
  emits: ['close-dialog'],
  methods: {
    cancel() {
      // 注册逻辑处理
      console.log('进入取消');
      this.$emit('close-dialog');  // 触发父组件的关闭对话框事件
    },
  },
  setup(props, { emit }) {
    const loginForm = reactive({
      username: '',
      password1: '',
      password2: '',
    });

    const rules = {
      username: [
        { required: true, message: '请输入用户名', trigger: 'blur' },
      ],
      password1: [
        { required: true, message: '请输入密码', trigger: 'blur' },
      ],
      password2: [
        { required: true, message: '请输入密码', trigger: 'blur' },
      ],
    };

    const loginFormRef = ref(null);

    const router = useRouter();
    const toRegisterPage = () => {
      router.push({ name: 'Register' })
    }
    const toHome = () => {
      router.push({ name: 'Home' })
    }

    const baseURL = import.meta.env.VITE_API_BASE_URL;
    const onSubmit = () => {
      loginFormRef.value.validate(() => {
        if (loginForm.password1 === loginForm.password2 && loginForm.password1 && loginForm.username) {
          const username = loginForm.username;
          const password = loginForm.password1;
          const loginFormJson = JSON.stringify({ username, password })
          console.log(loginFormJson)
          axios.post(`${baseURL}api/users/register/`, loginFormJson, {
            headers: {
              'Content-Type': 'application/json'
            }
          }).then(response => {
            if (response.status === 201) {
              ElMessage.success("注册成功");
              // toHome();
              emit('close-dialog');
            }
            else {
              ElMessage.error("该用户名已被注册");
            }
          }).catch(error => {
            ElMessage.error('注册失败');
            console.error('注册失败', error);
          })
        } else {
          ElMessage.error('密码输入不一致')
          console.log('验证失败');
          return;
        }
      })
    };
    return {
      loginForm,
      rules,
      loginFormRef,
      toRegisterPage,
      onSubmit,
    };
  },
});
</script>

<style scoped>
.RegisterButton {
  background: linear-gradient(90deg, #3b82f6, #06b6d4);
  color: #fff;
  font-weight: bold;
  border-radius: 5px;
  height: 45px;
}

.login-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
  /* 调整这个值来改变间距 */
}

.below-buttons {
  display: flex;
  /* margin-top: 10px; */
  justify-content: center;
}

.login-card {
  background-color: rgb(245, 241, 235);
}
</style>

<!-- <script>
const onSubmit = () => {
  if (loginFormRef.value) {
    console.log(loginFormRef.value)
    loginFormRef.value.validate((valid) => {
      if (valid && loginForm.password1 === loginForm.password2) {
        if (loginForm.password1 === loginForm.password2) {

          // 在这里处理登录逻辑，例如调用API
          const loginFormJson = JSON.stringify(loginForm);
          
          console.log(loginFormJson);


          axios.post(`${baseURL}api/users/register/`, loginFormJson, {
            headers: {
              'Content-Type': 'application/json'
            }
          }).then(response => {
            if(response.status===201){
              ElMessage.success("注册成功");
              // toHome();
              emit('close-dialog');
            }
            else{
              ElMessage.error("该用户名已被注册");
            }
          }).catch(error => {
            ElMessage.error('注册失败');
            console.error('注册失败', error);
          })
        } else {
          // ElMessage.error('密码输入不一致')
        }
        // 在这里处理登录逻辑，例如调用API
        // 示例：重置表单
        // loginFormRef.value.resetFields();
      } else {
        ElMessage.error('密码输入不一致')
        console.log('验证失败');
        return;
      }
    });
  }
};
</script> -->