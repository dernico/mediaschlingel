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
              "scripts/init.js",
              "scripts/jquery.mobile-1.3.2.min.js",
              "scripts/knockout-2.2.1.js",
              "scripts/linq.js",
              "scripts/ko.Page.js",
              "models/**/*.js",
              "data/**/*.js",
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
              'viewmodels/*.js', 
              'data/*.js', 
              'models/*.js', 
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

    watch: {
      files: ['<%= jshint.files %>'],
      tasks: ['jshint', 'qunit', 'concat', 'uglify']
    }
  });

  grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.loadNpmTasks('grunt-contrib-jshint');
  grunt.loadNpmTasks('grunt-contrib-qunit');
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-contrib-concat');

  //grunt.registerTask('test', ['jshint', 'qunit']);
  grunt.registerTask('test', ['jshint', 'qunit']);

  //grunt.registerTask('default', ['jshint', 'qunit', 'concat', 'uglify']);
  grunt.registerTask('default', ['jshint', 'qunit', 'concat', 'uglify']);

};