import bpy, re, os, importlib

bl_info = {
    "name": "Camera Scene Updater",
    "description": "Change scene parameters, like render resolution, using data in the camera name.",
    "author": "Oliver Etchebarne - http://drmad.org",
    "wiki_url": "https://github.com/drmad/camera-scene-tracker",
    "tracker_url": "https://github.com/drmad/camera-scene-tracker/issues",
    "version": (1,0),
    "category": "Scene",
    "location": "View 3D > Ctrl + Shift + NUMPAD_0"
}

addon_keymaps = []

class CameraSceneUpdater(bpy.types.Operator):
    bl_idname = "object.camera_scene_updater"
    bl_label = "Camera Scene Updater"
    bl_options = {'REGISTER', 'UNDO'}

    
    def execute(self, context):
        obj = context.object
        scene = bpy.context.scene
        
        # El objeto actual se convierte en la cámara activa
        scene.camera = obj
        
        bpy.ops.view3d.viewnumpad(type='CAMERA')

        name = obj.name
        
        match = re.search(r'\[(.+?)\]', name)
        if match:
            vars = match.group(1).split(':')
            
            for var in vars:
                cmd = var[0]
                args = var[1:]
                
                if cmd == 'c':
                    # Callback
                    
                    # Esto solo soporta module.function
                    modulename, function = args.split('.')
                    module = __import__(modulename)
                    # Just in case
                    importlib.reload(module)
                    callable = getattr(module, function)
                    callable(scene.camera)
                elif cmd == 'r':
                    # Resolución
                    res = args.split('x')
                    scene.render.resolution_x = int(res[0])
                    scene.render.resolution_y = int(res[1])
                elif cmd == 'p':
                    # Porcentaje de la resolucion
                    scene.render.resolution_percentage = int(args)
                elif cmd == 'f':
                    # Frames de inicio:fin
                    res = args.split('-')

                    if bool(res[0]):
                        scene.frame_start = int(res[0])
                    if len(res) == 2 and bool(res[1]):
                        scene.frame_end = int(res[1])
                elif cmd == 's':
                    # Cycles Samples
                    scene.cycles.samples = int(args)
                elif cmd == 'o':
                    # Directorio de salida
                                      
                    if args == "":
                        # Removemos el último componente de la salida, añadimos
                        # el nombre de la cámara

                        output_name = name[0:name.index('[')]
                        filepath = scene.render.filepath

                        abspath = filepath[0:2] == '//' 
                        if abspath:
                            filepath = filepath[2:]
                        
                        # Nos deshacemos del último '/'
                        filepath = filepath.rstrip(os.sep)

                        parts = filepath.split(os.sep)
                        
                        newparts = parts[0:-1]
                        newparts.append(output_name + os.sep)
                    
                        filepath = ('//' if abspath else '') + os.sep.join(newparts)
                    else:
                        filepath = args
                        
                    # Rearmamos el filepath

                    scene.render.filepath = filepath                    

        return {'FINISHED'}
    
def register():
    
    # Añadimos un keymap
    km = bpy.context.window_manager.keyconfigs.addon.keymaps.new(name='Object Mode')
    
    kmi = km.keymap_items.new(CameraSceneUpdater.bl_idname, 'NUMPAD_0', 'PRESS', shift=True, ctrl=True)
    #kmi.properties.total = 
    
    addon_keymaps.append(km)
    
    bpy.utils.register_class(CameraSceneUpdater)
    
def unregister():
    # Borramos los keymaps
    wm = bpy.context.window_manager
    for km in addon_keymaps:
        wm.keyconfigs.addon.keymaps.remove(km)

    addon_keymaps.clear()
            
    bpy.utils.unregister_class(CameraSceneUpdater)    
    
    
if __name__ == '__main__':
    register()
