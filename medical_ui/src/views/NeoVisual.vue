<template>
	<div>
        <el-card class="box-card">
            <div class="header">
                <el-form :model="formInline" >
                    <el-row class="demo-form-inline">
                        <el-form-item>
                            <el-input v-model="formInline.input" placeholder="请输入疾病名称" style="width:240px;"></el-input>
                            <el-select v-model="value2" placeholder="请选择实体类别" style="margin-left:5px;">
                                <el-option
                                    v-for="(item,index) in options3"
                                    :key="index"
                                    :label="item.label"
                                    :value="item.value2">
                                </el-option>
                            </el-select>
                            <el-select v-model="value" placeholder="请选择查询关系" style="margin-left:5px">
                                <el-option
                                    v-for="(item,index) in options1"
                                    :key="index"
                                    :label="item.label"
                                    :value="item.value">
                                </el-option>
                            </el-select>
                            <el-select v-model="value1" placeholder="请选择关联关系" style="margin-left:5px">
                                <el-option
                                    v-for="(item,index) in options2"
                                    :key="index"
                                    :label="item.label"
                                    :value="item.value1">
                                </el-option>
                            </el-select>
                        </el-form-item>
                        <el-form-item class="btn">
                            <el-button :disabled="isClicked" type="primary" icon="el-icon-search" @click="submit">搜索</el-button>
                        </el-form-item>
                    </el-row>
                </el-form>                  
            </div>
            <div class="myDiv">
                <div id="viz" ref="viz"></div>
            </div>
            <div class="myList">
                <div class="table">
                    <el-table :data="tableData.slice((currentPage-1)*pageSize,currentPage*pageSize)" stripe style="width: 100%">
                        <el-table-column prop="diseasename" label="实体" width="200" align="center"></el-table-column>
                        <el-table-column prop="relationship" label="关系" width="200" align="center"></el-table-column>
                        <el-table-column prop="node" label="属性" width="180" align="center"></el-table-column>
                    </el-table>
                    <div class="block">
                        <el-pagination
                            layout="total, prev, pager, next"
                            :total="tableData.length"
                            align="center"
                            :current-page="currentPage"
                            :page-size="pageSize"
                            @current-change="handleCurrent"
                        >
                        </el-pagination>
                    </div>
                </div>
            </div>
	    </el-card>
	</div>
</template>

<script>
import NeoVis from 'neovis.js';
import neo4j from 'neo4j-driver'
export default {
    name: 'NeoVisual',
    data () {
        return {
            formInline: {
                input: ''
            },
            viz: {}, // 定义一个viz对象,
            cypher:'',
            // 是否点击该按钮
            isClicked: true,
            value:'',//拿到用户所选择的关系
            value1:'',
            value2:'',
            tableData:[],//数据库返回结果存放
            currentPage:1,//分页当前页面
            pageSize:11,//每页展示的数据
            options1: [
                {
                    value: 0,
                    label: 'all relationship所有关系'
                },
                {
                    value: 'belongs_to',
                    label: 'belongs_to属于'
                },
                {
                    value: 'acompany_with',
                    label: 'acompany_with伴随疾病'
                },
                {
                    value: 'cure_department',
                    label: 'cure_department科室'
                },
                {
                    value:'do_eat',
                    label:'do_eat宜吃食物'
                },
                {
                    value:'has_common_drug',
                    label:'has_common_drug常用药物'
                },
                {
                    value:'has_symptom',
                    label:'has_symptom有什么症状'
                },
                {
                    value:'need_check',
                    label:'need_check需要的检查'
                },
                {
                    value:'not_eat',
                    label:'not_eat不宜吃'
                },
                {
                    value:'production',
                    label:'production制药商'
                },
                {
                    value:'recommand_drug',
                    label:'recommand_drug推荐药物'
                },
                {
                    value:'recommand_recipes',
                    label:'recommand_recipes推荐食谱'
                }
            ],
            options2:[
                {
                    value1:0,
                    label:'所有关联'
                },
                {
                    value1:1,
                    label:'主动关联'
                },
                {
                    value1:2,
                    label:'被动关联'
                }
            ],
            options3:[
                {
                    value2:'疾病',
                    label:'疾病'
                },
                {
                    value2:'症状',
                    label:'症状'
                },
                {
                    value2:'科室',
                    label:'科室'
                }
            ],
            englishToChinese: {
                "belongs_to": "属于",
                "acompany_with": "伴随",
                "cure_department": "治疗科室",
                "do_eat": "推荐食物",
                "has_common_drug": "常见药品",
                "has_symptom": "症状",
                "need_check": "需要检查",
                "not_eat": "禁忌食物",
                "production": "制造商",
                "recommand_drug": "推荐药品",
                "recommand_recipes": "推荐菜品"
            }
        }
    },
    methods: {
        submit () {
            if(this.value===0){
                if(this.value1===0){
                    // this.cypher = `MATCH(p:疾病)-[r]-(q) WHERE p.name='${this.formInline.input}' RETURN p,r,q`
                    this.cypher = `MATCH(p:${this.value2})-[r]-(q) WHERE p.name='${this.formInline.input}' RETURN p,r,q`
                }
                else if(this.value1===1){
                    this.cypher = `MATCH(p:${this.value2})-[r]->(q) WHERE p.name='${this.formInline.input}' RETURN p,r,q`
                }
                else if(this.value1===2){
                    this.cypher = `MATCH(p:${this.value2})<-[r]-(q) WHERE p.name='${this.formInline.input}' RETURN p,r,q`
                }
            }
            else {
                if(this.value1===0){
                    this.cypher = `MATCH(p:${this.value2})-[r:${this.value}]-(q) WHERE p.name='${this.formInline.input}' RETURN p,r,q`
                }
                else if(this.value1===1){
                    this.cypher = `MATCH(p:${this.value2})-[r:${this.value}]->(q) WHERE p.name='${this.formInline.input}' RETURN p,r,q`
                }
                else if(this.value1===2){
                    this.cypher = `MATCH(p:${this.value2})<-[r:${this.value}]-(q) WHERE p.name='${this.formInline.input}' RETURN p,r,q`
                }
            }
            
            this.search()
            .then((length) => {
                if(length){
                    this.viz.renderWithCypher(this.cypher);
                } 
                else {
                    this.$message.error("当前疾病不存在该关系，请重新选择！");
                    this.tableData=[]
                }
            })
        },
        draw(){
            var config ={
                containerId: 'viz',
                neo4j: {
                    serverUrl: 'bolt://localhost:7687',
                    serverUser: 'neo4j',
                    serverPassword: ''
                },
                labels: {
                    科室:{
                        label: 'name',  // 节点显示的文字对应内容key
                        // community: 'community', //节点颜色 String：要用作社区（color）的属性名。默认为“按标签着色”。
                        // size: 'pagerank',  // 用作节点大小的属性名。默认为1。
                    },
                    检查:{label: 'name'},
                    疾病:{label: 'name'},
                    症状:{label: 'name'},
                    药企:{label: 'name'},
                    药品:{label: 'name'},
                    菜谱:{label: 'name'},
                    食物:{label: 'name'},
                },
                relationships: {
                    belongs_to: {label: "name"},
                    acompany_with: {label: "name"},
                    cure_department:{label: "name"},
                    do_eat:{label: "name"},
                    has_common_drug:{label: "name"},
                    has_symptom:{label: "name"},
                    need_check:{label: "name"},
                    not_eat:{label: "name"},
                    production:{label: "name"},
                    recommand_drug:{label: "name"},
                    recommand_recipes:{label: "name"},
                },
                visConfig: {
                    edges: {
                        arrows: {
                            to: {enabled: true}
                        }
                    }
                },
                initialCypher: "MATCH (p)-[r]->(m) RETURN p, r, m limit 50"
            }
            this.viz = new NeoVis(config)
            // console.log(this.viz);
            this.viz.render()
            // 点击完搜索全图之后 才能开启搜索功能，因为需要先渲染一下
            this.isClicked = false            
        },
        search(){
            return new Promise((resolve,reject)=>{
                this.tableData = []
                const driver = neo4j.driver("bolt://localhost:7687",neo4j.auth.basic("neo4j",""))
                const session = driver.session()
                session.run(this.cypher)
                .then((res)=>{
                    console.log(res);
                    this.tableData = []
                    if(this.value1===0 || this.value1===1){
                        for(let i=0;i<res.records.length;i++){
                            this.tableData.push
                            ({
                                diseasename:res.records[i]._fields[0].properties.name,
                                relationship:this.englishToChinese[res.records[i]._fields[1].properties.name],
                                node:res.records[i]._fields[2].properties.name
                            })
                        }                        
                    }
                    else if(this.value1===2){
                        for(let i=0;i<res.records.length;i++){
                            this.tableData.push
                            ({
                                diseasename:res.records[i]._fields[2].properties.name,
                                relationship:this.englishToChinese[res.records[i]._fields[1].properties.name],
                                node:res.records[i]._fields[0].properties.name,
                            })
                        }
                    }
                    // 成功时将长度值返回，使用resolve即可返回
                    resolve(this.tableData.length)
                })
            })
        },
        handleCurrent(val){
            this.currentPage = val
        }
    },
    mounted(){
        this.draw()
    }
}
</script>

<style lang='less' scoped>
.box-card {
    .header{
        width: 100%;
        .demo-form-inline{
            display: flex;
            .btn{
                margin-left: 55px;
                width: 100px;
            }                 
        }        
    }
    .myDiv {
        width: 800px;
        height: 800px;
        float: left;
        #viz {
            width: 800px;
            height: 80%;
            border: 1px solid #000;
            font: 22pt;
        }        
    }
    .myList{
        float: right;
        .table{
            overflow-y: auto;
            width: 600px;
            height: 640px;
            border:1px solid #000;
        }
    }
}
</style>
