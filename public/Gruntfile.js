module.exports = function(grunt) {
  
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    
    concat: {
      options: {
        separator: ';'
      },
      dist: {
        src: [
              //include
              "scripts/jquery.min.js",
              //"scripts/init.js",
              //"scripts/jquery.mobile-1.3.2.min.js",
              "scripts/knockout-2.2.1.js",
              "scripts/linq.js",
              "scripts/Page.js",
              "scripts/trunk.js",
              "scripts/pushy/js/pushy.min.js",
              "models/**/*.js",
              "data/**/*.js",
              "services/**/*.js",
              "viewmodels/**/*.js"
              //exclude
              //'!app/lib/**/*.min.js',
              //'!app/js/**/*.min.js'
            ],
        dest: 'dist/<%= pkg.name %>.js'
      }
    },
    
    uglify: {
      options: {
        banner: '/*! <%= pkg.name %> <%= grunt.template.today("dd-mm-yyyy") %> */\n'
      },
      dist: {
        files: {
          'dist/<%= pkg.name %>.min.js': ['<%= concat.dist.dest %>']
        }
      }
    },
    
    qunit: {
      files: ['test/specs/**/*.html']
    },
    jshint: {
      files: ['Gruntfile.js',
              'viewmodels/**/*.js', 
              'data/**/*.js', 
              'models/**/*.js', 
              'test/specs/**/*.js'],
      options: {
        // options here to override JSHint defaults
        globals: {
          sinon: true,
          jQuery: true,
          console: true,
          module: true,
          document: true
        }
      }
    },
    less:{
      production:{
        options: {
          paths: "css",
          cleancss: true
        },
        files:{
          'css/app.css' : 'css/app.less'
        }
      }
    },
    watch: {
      files: ['scripts/Page.js', '<%= jshint.files %>', 'css/**/*.less'],
      //tasks: ['jshint', 'concat', 'less', 'uglify']
      tasks: ['jshint', 'concat', 'uglify']
    }
  });

  grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.loadNpmTasks('grunt-contrib-jshint');
  //grunt.loadNpmTasks('grunt-contrib-qunit');
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-contrib-concat');
  //grunt.loadNpmTasks('grunt-contrib-less');


  //grunt.registerTask('test', ['jshint', 'qunit']);
  grunt.registerTask('test', ['jshint']);

  //grunt.registerTask('default', ['jshint', 'qunit', 'concat', 'uglify']);
  grunt.registerTask('default', ['jshint', 'concat', 'uglify']);

};