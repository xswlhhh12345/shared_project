import{r as c,o as s,c as r,a as o,F as u,g as i}from"./index-d8bd3db5.js";const f={__name:"AboutView",setup(g){const t=c(null),n=e=>{t.value=e.target.files[0],console.log(e.target)},l=async()=>{const e=new FormData;e.append("file",t.value),await i(e).then(a=>{console.log(a.data)}).catch(a=>{console.log(a)})};return(e,a)=>(s(),r(u,null,[o("input",{type:"file",onChange:n},null,32),o("button",{onClick:l},"上传图片")],64))}};export{f as default};