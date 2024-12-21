<template>
  <div class="login-container">
    <el-card class="login-card" shadow="never">

      <h2 class="login-title">用户登录</h2>

      <el-form class="Form" :model="loginForm" :rules="rules" ref="loginFormRef" label-width="80px"
        label-position="left">

        <el-form-item label="用户名" prop="username">
          <el-input  label="用户名" v-model="loginForm.username" placeholder="请输入用户名"></el-input>
        </el-form-item>

        <el-form-item  label="密码" prop="password">
          <el-input  v-model="loginForm.password" type="password" placeholder="请输入密码"></el-input>
        </el-form-item>
        <div class="below-buttons">
          <el-button class="LoginButton" type="primary" @click="onSubmit">登录</el-button>
          <el-button class="RegisterButton" tag="a" @click="dialogVisible = true">注册</el-button>
          <el-dialog class="dialog" v-model="dialogVisible" width="480" align-center>
            <Register @close-dialog="close_dialog"></Register>
          </el-dialog>
        </div>
      </el-form>
    </el-card>
  </div>
</template>

<script>
import { defineComponent, inject, reactive, ref } from 'vue';
import Register from './Register.vue';
import { ElForm, ElMessage } from 'element-plus';
import axios from 'axios';
import { useRouter } from 'vue-router';

export default defineComponent({
  components: {
    Register,
  },
  emits: ['closeDialog'],
  name: 'Login',
  methods: {
    close(){
      this.$emit('closeDialog');
    }
  },
  setup(props, { emit }) {
    const dialogVisible = ref(false);
    const loginForm = reactive({
      username: '',
      password: '',
    });
    const rules = {
      username: [
        { required: true, message: '请输入用户名', trigger: 'blur' },
      ],
      password: [
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

    const close_dialog = () => {
      console.log('1');
      dialogVisible.value = false;
    }

    const baseURL = import.meta.env.VITE_API_BASE_URL;
    console.log(baseURL)
    const onSubmit = () => {
      const loginFormJson = JSON.stringify(loginForm);
      console.log(loginFormJson);
      if (loginFormRef.value) {
        loginFormRef.value.validate((valid) => {
          if (valid) {
            axios.post(`${baseURL}api/users/login/`, loginFormJson, {
              headers: {
                'Content-Type': 'application/json'
              }
            }).then(
              response => {
                if (response.status === 200) {//这个返回值是否为200？
                  ElMessage.success("登录成功");
                  emit('closeDialog');
                  console.log('登录成功', loginForm);
                  //存储用户id ，这里是否应该转为存储token
                  loginForm.username='';
                  loginForm.password='';
                  localStorage.setItem('token',response.data.token);
                  console.log(localStorage.getItem('token'));
                }
                else {
                  ElMessage.error("登录失败");
                  loginForm.username='';
                  loginForm.password='';
                  return;
                }
              }).catch(error => {
                ElMessage.error("登录失败")
                console.error('登录失败', error);
              })
            // 示例：重置表单
            // loginFormRef.value.resetFields();
          } else {
            console.log('验证失败');
            return;
          }
        });
      }
    };

    return {
      loginForm,
      rules,
      loginFormRef,
      onSubmit,
      toRegisterPage,
      dialogVisible,
      close_dialog,
    };
  },
});
</script>

<style scoped>
.dialog {
  height: 200px;
  overflow-y: auto;
  background-color: rgb(229, 225, 221);
}

.login-card {
  background-color: rgb(245, 241, 235);
}

.LoginButton {
  background: linear-gradient(90deg, #3b82f6, #06b6d4);
  color: #fff;
  font-weight: bold;
  border-radius: 5px;
  height: 45px;
}

.RegisterButton {
  background: linear-gradient(90deg, #3b82f6, #06b6d4);
  color: #fff;
  font-weight: bold;
  border-radius: 5px;
  height: 45px;
}

.below-buttons {
  display: flex;
  justify-content: center;
}
</style>
