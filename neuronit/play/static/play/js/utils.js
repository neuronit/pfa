<!-- Button js  -->
var add_edge = false,
    add_vertex = false,
    delete_edge = false,
    delete_vertex = false;

function change_addEdge() {
    if (!document.getElementById("add_edge").classList.contains('active')) {
        add_edge = true;
        add_vertex = false;
        delete_edge = true;
        delete_vertex = false;
        document.getElementById("add_edge").classList.add('active');
    }
    else {
        add_edge = false;
        document.getElementById("add_edge").classList.remove('active');
    }

    document.getElementById("add_vertex").classList.remove('active');
    document.getElementById("delete_vertex").classList.remove('active');
    document.getElementById("delete_edge").classList.remove('active');
};

function change_addVertex() {
    if (!document.getElementById("add_vertex").classList.contains('active')) {
        add_edge = false;
        add_vertex = true;
        delete_edge = false;
        delete_vertex = false;
        document.getElementById("add_vertex").classList.add('active');

    }
    else {

        add_vertex = false;
        document.getElementById("add_vertex").classList.remove('active');

    }

    document.getElementById("add_edge").classList.remove('active');
    document.getElementById("delete_vertex").classList.remove('active');
    document.getElementById("delete_edge").classList.remove('active');
};

function change_deleteEdge() {
    if (!document.getElementById("delete_edge").classList.contains('active')) {
        add_edge = false;
        add_vertex = false;
        delete_edge = true;
        delete_vertex = false;
        document.getElementById("delete_edge").classList.add('active');

    }
    else {

        delete_edge = false;
        document.getElementById("delete_edge").classList.remove('active');

    }

    document.getElementById("add_edge").classList.remove('active');
    document.getElementById("add_vertex").classList.remove('active');
    document.getElementById("delete_vertex").classList.remove('active');
};


function change_deleteVertex() {
    if (!document.getElementById("delete_vertex").classList.contains('active')) {

        add_edge = false;
        add_vertex = false;
        delete_edge = false;
        delete_vertex = true;
        document.getElementById("delete_vertex").classList.add('active');

    }
    else {

        delete_vertex = false;
        document.getElementById("delete_vertex").classList.add('active');
    }

    document.getElementById("add_edge").classList.remove('active');
    document.getElementById("add_vertex").classList.remove('active');
    document.getElementById("delete_edge").classList.remove('active');
};
