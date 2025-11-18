const axios = require('axios')


const baseUrl = "https://www.tcgweb.cn"

/**
 * 存储
 * @param userName
 * @param password
 */

const  setUser = async (userName , password) =>{

    let userData = {
        userId : userName,
        password: password,
        username : null,
        userTel : null,
        userEmail : null,
        userAvatarUrl : null
    }
    const options = {
        method: 'POST',
        headers: { 'content-type': 'application/x-www-form-urlencoded' },
        data: userData,
        url :"http://www.tcgweb.cn:80/login" ,
    };
    return new Promise((resolve, reject) => {
        axios(options).then((res) => {
            resolve(res.data)
        }).catch(err => {
            if(err) reject(err)
        })
    })
}

/**
 * 获取
 */
const getUser = async () => {
    return new Promise((resolve, reject) => {
        axios
            .post(`http://www.tcgweb.cn:80/test`)
            .then((res) => {
                console.log(res)
                if (res.data !== -1) {
                    resolve(1);
                } else {
                    resolve(0);
                }
            })
            .catch((err) => {
                console.log(err);
                reject(err);
            });
    });
};


/**
 * 删除
 */
const delUser = async () => {
    try {
        const res = await axios.post('http://www.tcgweb.cn:80/logout');
        if (res.data.mscr === '成功') {
            // console.log(res.data.mscr);
            return true;
        } else {
            return false;
        }
    } catch (error) {
        console.error(error);
        return false;
    }
};

module.exports = {
    baseUrl,
    setUser,
    getUser,
    delUser
}

// TODO 获取用户凭证